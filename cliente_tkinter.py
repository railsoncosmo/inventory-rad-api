import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://localhost:5001"
FONT_FAMILY = "Helvetica"


def form_button(parent, text, command):
  btn = tk.Label(
    parent,
    text=text,
    font=(FONT_FAMILY, 12, "bold"),
    bg="black",
    fg="white",
    padx=20,
    pady=8,
    cursor="hand2",
  )
  btn.bind("<Button-1>", lambda _event: command())
  return btn


def action_button(parent, text, command):
  btn = tk.Label(
    parent,
    text=text,
    font=(FONT_FAMILY, 10, "bold"),
    bg="black",
    fg="white",
    padx=8,
    pady=4,
    cursor="hand2",
  )
  btn.bind("<Button-1>", lambda _event: command())
  return btn


class CreateProductView(tk.Frame):
  FIELD_WIDTH = 40
  PRODUCT_FIELDS = (
    ("name", "Nome do Produto"),
    ("category", "Categoria"),
    ("quantity", "Quantidade"),
    ("price", "Preço"),
  )

  def __init__(self, parent, root_app):
    super().__init__(parent, bg="white")
    self.root_app = root_app
    self.editing_id = None

    self.title_label = tk.Label(self, text="Cadastro", font=(FONT_FAMILY, 18, "bold"), bg="black")
    self.title_label.pack(pady=(20, 30))

    center = tk.Frame(self, bg="white")
    center.pack(expand=True, fill="both")

    form = tk.Frame(center, bg="white")
    form.pack(anchor="center", expand=True)

    self.fields = {}
    for key, attribute in self.PRODUCT_FIELDS:
      field_frame = tk.Frame(form, bg="white")
      field_frame.pack(pady=10, anchor="center")

      tk.Label(
        field_frame,
        text=attribute,
        font=(FONT_FAMILY, 11, "bold"),
        bg="white",
        fg="#374151",
        anchor="w",
        width=self.FIELD_WIDTH,
      ).pack(anchor="w")

      entry = tk.Entry(field_frame, font=(FONT_FAMILY, 12), width=self.FIELD_WIDTH)
      entry.pack(anchor="w")
      self.fields[key] = entry

    buttons = tk.Frame(center, bg="white")
    buttons.pack(pady=(10, 40), anchor="center")

    form_button(buttons, "Salvar", self.save_product).pack(side="left", padx=10)
    form_button(buttons, "Cancelar", self.cancel).pack(side="left", padx=10)

  def clear_form(self):
    for entry in self.fields.values():
      entry.delete(0, tk.END)

  def reset(self):
    self.editing_id = None
    self.title_label.config(text="Cadastro", bg="black")
    self.clear_form()

  def cancel(self):
    self.reset()
    self.root_app.show_view("list")

  def load_for_edit(self, product):
    self.editing_id = product.get("id")
    self.title_label.config(text="Editar Produto")
    self.fields["name"].delete(0, tk.END)
    self.fields["name"].insert(0, product.get("name", ""))
    self.fields["category"].delete(0, tk.END)
    self.fields["category"].insert(0, product.get("category", ""))
    self.fields["quantity"].delete(0, tk.END)
    self.fields["quantity"].insert(0, str(product.get("quantity", "")))
    self.fields["price"].delete(0, tk.END)
    self.fields["price"].insert(0, str(product.get("price", "")))

  def save_product(self):
    name = self.fields["name"].get().strip()
    category = self.fields["category"].get().strip()
    quantity = self.fields["quantity"].get().strip()
    price = self.fields["price"].get().strip()

    if not name or not category or not quantity or not price:
      messagebox.showwarning("Atenção", "Preencha todos os campos.")
      return

    try:
      quantity_int = int(quantity)
      price_float = float(price)
    except ValueError:
      messagebox.showwarning("Atenção", "Quantidade e preço devem ser números válidos.")
      return

    data = {
      "name": name,
      "category": category,
      "quantity": quantity_int,
      "price": price_float,
    }

    try:
      if self.editing_id:
        response = requests.put(f"{API_URL}/products/{self.editing_id}", json=data, timeout=5)
        success_status = 200
        success_message = "Produto atualizado com sucesso!"
      else:
        response = requests.post(f"{API_URL}/products", json=data, timeout=5)
        success_status = 201
        success_message = "Produto criado com sucesso!"

      if response.status_code == success_status:
        messagebox.showinfo("Sucesso", success_message)
        self.reset()
        self.root_app.show_view("list")
      else:
        messagebox.showerror("Erro", f"Não foi possível salvar o produto. ({response.status_code})")
    except requests.RequestException:
      messagebox.showerror("Erro", "Não foi possível conectar ao servidor. Verifique se o Flask está rodando.")


def format_price(price):
  value = f"{float(price):,.2f}"
  return f"R$ {value.replace(',', 'X').replace('.', ',').replace('X', '.')}"


class ProductRow(tk.Frame):
  COLUMN_WIDTHS = (200, 120, 90, 90, 150)

  def __init__(self, parent, product, list_view):
    super().__init__(parent, bg="white")
    self.pack(fill="x")

    border = tk.Frame(self, bg="#e9ecef", height=1)
    border.pack(fill="x", side="bottom")

    row = tk.Frame(self, bg="white", padx=16, pady=14)
    row.pack(fill="x")

    for col, width in enumerate(self.COLUMN_WIDTHS):
      row.grid_columnconfigure(col, minsize=width, weight=0)

    name_text = tk.Frame(row, bg="white")
    name_text.grid(row=0, column=0, sticky="w")
    tk.Label(name_text, text="›", font=(FONT_FAMILY, 12), fg="#9ca3af", bg="white").pack(side="left")
    tk.Label(
      name_text, text=product.get("name", ""), font=(FONT_FAMILY, 11, "bold"),
      fg="#111827", bg="white",
    ).pack(side="left", padx=(4, 0))

    tk.Label(
      row, text=product.get("category", ""), font=(FONT_FAMILY, 11),
      fg="#6b7280", bg="white", anchor="w",
    ).grid(row=0, column=1, sticky="w")

    tk.Label(
      row, text=product.get("quantity", ""), font=(FONT_FAMILY, 11),
      fg="#6b7280", bg="white", anchor="w",
    ).grid(row=0, column=2, sticky="w")

    tk.Label(
      row, text=format_price(product.get("price", 0)), font=(FONT_FAMILY, 11, "bold"),
      fg="#111827", bg="white", anchor="w",
    ).grid(row=0, column=3, sticky="w")

    actions = tk.Frame(row, bg="white")
    actions.grid(row=0, column=4, sticky="w")
    action_button(actions, "Editar", lambda: list_view.edit_product(product)).pack(side="left", padx=(0, 6))
    action_button(actions, "Remover", lambda: list_view.remove_product(product)).pack(side="left")


class ListProductsView(tk.Frame):
  HEADER_BG = "#f3f4f6"
  HEADER_FG = "#9ca3af"
  COLUMN_WIDTHS = ProductRow.COLUMN_WIDTHS
  COLUMNS = (
    ("NOME DO PRODUTO", 0),
    ("CATEGORIA", 1),
    ("QUANTIDADE", 2),
    ("PREÇO", 3),
    ("AÇÕES", 4),
  )

  def __init__(self, parent, root_app):
    super().__init__(parent, bg="white")
    self.root_app = root_app

    page_header = tk.Frame(self, bg="white")
    page_header.pack(fill="x", padx=20, pady=(20, 16))

    tk.Label(
      page_header, text="Listagem de Produtos", font=(FONT_FAMILY, 18, "bold"),
      bg="white", fg="#111827",
    ).pack(side="left")

    filter_bar = tk.Frame(self, bg="white")
    filter_bar.pack(fill="x", padx=20, pady=(0, 12))

    tk.Label(
      filter_bar, text="Filtro", font=(FONT_FAMILY, 11, "bold"),
      bg="white", fg="#374151",
    ).pack(side="left", padx=(0, 8))

    self.filter_entry = tk.Entry(filter_bar, font=(FONT_FAMILY, 11), width=30)
    self.filter_entry.pack(side="left", padx=(0, 8))
    self.filter_entry.bind("<Return>", lambda _e: self.refresh())

    form_button(filter_bar, "Buscar", self.refresh).pack(side="left")
    form_button(filter_bar, "Limpar filtro", self.clear_filter).pack(side="left", padx=(8, 0))

    table_container = tk.Frame(self, bg="white", highlightbackground="#e5e7eb", highlightthickness=1)
    table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    self._build_table_header(table_container)

    body = tk.Frame(table_container, bg="white")
    body.pack(fill="both", expand=True)

    self.canvas = tk.Canvas(body, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(body, orient="vertical", command=self.canvas.yview)
    self.rows_frame = tk.Frame(self.canvas, bg="white")

    self.rows_frame.bind(
      "<Configure>",
      lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
    )
    self.canvas_window = self.canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
    self.canvas.configure(yscrollcommand=scrollbar.set)
    self.canvas.bind("<Configure>", self._on_canvas_configure)

    self.canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    self.canvas.bind("<Enter>", self._bind_mousewheel)
    self.canvas.bind("<Leave>", self._unbind_mousewheel)

  def _on_canvas_configure(self, event):
    self.canvas.itemconfig(self.canvas_window, width=event.width)

  def _bind_mousewheel(self, _event):
    self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
    self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

  def _unbind_mousewheel(self, _event):
    self.canvas.unbind_all("<MouseWheel>")
    self.canvas.unbind_all("<Button-4>")
    self.canvas.unbind_all("<Button-5>")

  def _on_mousewheel_linux(self, event):
    if event.num == 4:
      self.canvas.yview_scroll(-1, "units")
    elif event.num == 5:
      self.canvas.yview_scroll(1, "units")

  def _on_mousewheel(self, event):
    if self.winfo_ismapped():
      self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

  def _build_table_header(self, parent):
    header = tk.Frame(parent, bg=self.HEADER_BG, padx=16, pady=12)
    header.pack(fill="x")

    for col, width in enumerate(self.COLUMN_WIDTHS):
      header.grid_columnconfigure(col, minsize=width, weight=0)

    for label, index in self.COLUMNS:
      tk.Label(
        header, text=label, font=(FONT_FAMILY, 9, "bold"),
        fg=self.HEADER_FG, bg=self.HEADER_BG, anchor="w",
      ).grid(row=0, column=index, sticky="w")

  def _show_message(self, text, show_retry=False):
    for widget in self.rows_frame.winfo_children():
      widget.destroy()

    frame = tk.Frame(self.rows_frame, bg="white")
    frame.pack(pady=40)

    tk.Label(
      frame, text=text, font=(FONT_FAMILY, 12), fg="#6b7280", bg="white",
      justify="center",
    ).pack()

    if show_retry:
      form_button(frame, "Tentar novamente", self.refresh).pack(pady=(12, 0))

  def clear_filter(self):
    self.filter_entry.delete(0, tk.END)
    self.refresh()

  def refresh(self):
    for widget in self.rows_frame.winfo_children():
      widget.destroy()

    try:
      name_filter = self.filter_entry.get().strip()
      params = {"name": name_filter} if name_filter else {}
      response = requests.get(f"{API_URL}/products", params=params, timeout=5)
      if response.status_code != 200:
        messagebox.showerror("Erro", f"Não foi possível listar os produtos. ({response.status_code})")
        return

      products = response.json()
      if not products:
        self._show_message("Nenhum produto cadastrado.")
        return

      for product in products:
        ProductRow(self.rows_frame, product, self)

      self.rows_frame.update_idletasks()
      self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    except requests.RequestException:
      self._show_message(
        "Não foi possível conectar ao servidor.\n"
        "Inicie a API em outro terminal com:\npython app.py",
        show_retry=True,
      )

  def edit_product(self, product):
    self.root_app.show_view("create", product=product)

  def remove_product(self, product):
    product_name = product.get("name", "este produto")
    if not messagebox.askyesno("Confirmar", f"Deseja remover {product_name}?"):
      return

    try:
      response = requests.delete(f"{API_URL}/products/{product.get('id')}", timeout=5)
      if response.status_code == 200:
        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
        self.refresh()
      else:
        messagebox.showerror("Erro", f"Não foi possível remover o produto. ({response.status_code})")
    except requests.RequestException:
      messagebox.showerror("Erro", "Não foi possível conectar ao servidor. Verifique se o Flask está rodando.")


class Root:
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("Sistema de Gestão de Estoque RAD")
    self.root.geometry("1000x600")
    self.root.configure(bg="white")

    self.sidebar = tk.Frame(self.root, width=200, bg="black")
    self.sidebar.pack(side="left", fill="y")
    self.sidebar.pack_propagate(False)

    tk.Label(
      self.sidebar, text="Menu", font=(FONT_FAMILY, 14, "bold"),
      bg="black", fg="white",
    ).pack(pady=(20, 30))

    nav_style = {"font": (FONT_FAMILY, 11), "bg": "white", "fg": "black", "width": 16, "cursor": "hand2", "pady": 8}

    tk.Button(
      self.sidebar, text="Criar Produto",
      command=lambda: self.show_view("create"),
      **nav_style,
    ).pack(pady=5, padx=10)

    tk.Button(
      self.sidebar, text="Listar Produtos",
      command=lambda: self.show_view("list"),
      **nav_style,
    ).pack(pady=5, padx=10)

    self.content = tk.Frame(self.root, bg="white")
    self.content.pack(side="left", fill="both", expand=True)

    self.views = {
      "create": CreateProductView(self.content, self),
      "list": ListProductsView(self.content, self),
    }

    self.show_view("list")
    self.root.mainloop()

  def show_view(self, name, product=None):
    for view in self.views.values():
      view.pack_forget()

    self.views[name].pack(fill="both", expand=True)

    if name == "create":
      if product:
        self.views["create"].load_for_edit(product)
      else:
        self.views["create"].reset()

    if name == "list":
      self.views["list"].refresh()

cliente = Root()
