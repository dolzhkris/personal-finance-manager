import tkinter as tk #для графического интерфейса
from tkinter import ttk, messagebox #для графического интерфейса
from datetime import datetime #для работы с датой и временем
import matplotlib.pyplot as plt #для графиков
from PIL import Image, ImageTk #для иконки приложения

class Category: #класс для управления категориями
    def __init__(self):
        self.income_categories = ["Зарплата", "Подарки", "Инвестиции", "Прочее"]
        self.expense_categories = ["Еда", "Транспорт", "Развлечения", "Жилье", "Здоровье", "Прочее"]
    
    def get_categories(self, transaction_type): #возвращает категории в зависимости от типа операции
        if transaction_type == "Доход":
            return self.income_categories
        else:
            return self.expense_categories

class Expense: #класс для операций доходов и расходов
    def __init__(self, amount, description, category, transaction_type):
        self.date = datetime.now()
        self.amount = amount
        self.description = description
        self.category = category
        self.transaction_type = transaction_type

class RecurringExpense(Expense): #класс для периодических расходов
    def __init__(self, amount, description, category, frequency):
        super().__init__(amount, description, category, "Расход")
        self.frequency = frequency  #день, неделя, месяц

class User: #класс для пользователя
    def __init__(self, name):
        self.name = name
        self.transactions = []  #список объектов Expense
    
    def add_transaction(self, transaction): #добавляет операцию
        self.transactions.append(transaction)
    def get_balance(self): #возвращает текущий баланс
        income = sum(t.amount for t in self.transactions if t.transaction_type == "Доход")
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == "Расход")
        return income - expenses
    
    def get_transaction_history(self, limit=20): #возвращает историю операций
        return self.transactions[-limit:]
      
    def get_stats(self): #возвращает статистику по доходам, расходам и категориям
        income = sum(t.amount for t in self.transactions if t.transaction_type == "Доход")
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == "Расход")
        balance = income - expenses
        
        #статистика по категориям расходов
        expense_categories = {}
        for transaction in self.transactions:
            if transaction.transaction_type == "Расход":
                category = transaction.category
                expense_categories[category] = expense_categories.get(category, 0) + transaction.amount
        return {"income": income, "expenses": expenses, "balance": balance, "expense_categories": expense_categories}

class FinanceApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Учет финансов")

        icon = Image.open("icon.jpg")  # открываем изображение
        photo = ImageTk.PhotoImage(icon)
        self.root.iconphoto(False, photo)

        self.root.geometry("900x400")

        self.category_manager = Category()
        self.users = {"Димаш": User("Димаш")}
        self.current_user = "Димаш"
        
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        top_frame = ttk.Frame(self.root) #верхняя панель с выбором пользователя
        top_frame.pack(pady=10)
        
        ttk.Label(top_frame, text="Пользователь:").pack(side='left')
        self.user_var = tk.StringVar(value="Димаш")
        user_combo = ttk.Combobox(top_frame, textvariable=self.user_var, values=list(self.users.keys()))
        user_combo.pack(side='left', padx=5)
        user_combo.bind('<<ComboboxSelected>>', self.change_user)
        
        ttk.Button(top_frame, text="+", command=self.add_user, width=3).pack(side='left', padx=2)
        ttk.Button(top_frame, text="х", command=self.delete_user, width=3).pack(side='left', padx=2)

        notebook = ttk.Notebook(self.root) #основная область с вкладками
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        self.setup_add_tab(notebook)
        self.setup_history_tab(notebook)
        self.setup_stats_tab(notebook)

    def setup_add_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Добавить")
        
        ttk.Label(frame, text="Тип:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.type_var = tk.StringVar(value="Расход")
        ttk.Combobox(frame, textvariable=self.type_var, values=["Доход", "Расход"], state="readonly").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(frame, textvariable=self.category_var)
        self.category_combo.grid(row=1, column=1, padx=5, pady=5)
        self.update_categories()
        
        ttk.Label(frame, text="Сумма:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Описание:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.desc_entry = ttk.Entry(frame)
        self.desc_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Добавить", command=self.add_transaction).grid(row=4, column=0, columnspan=2, pady=10)
        
        self.type_var.trace('w', self.update_categories)

    def setup_history_tab(self, notebook): #вкладка истории операций
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="История")
        
        columns = ("Дата", "Тип", "Категория", "Описание", "Сумма")
        self.history_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def setup_stats_tab(self, notebook): #вкладка статистики
       frame = ttk.Frame(notebook)
        notebook.add(frame, text="Статистика")
        
        self.stats_text = tk.Text(frame, height=10, width=60)
        self.stats_text.pack(pady=10)
        
        ttk.Button(frame, text="Показать график", command=self.show_chart).pack()

    def update_categories(self, *args): #обновляет список категорий в зависимости от типа операции
        categories = self.category_manager.get_categories(self.type_var.get())
        self.category_combo['values'] = categories
        if categories:
            self.category_combo.set(categories[0])
 
    def add_user(self): #добавляет нового пользователя
        name = tk.simpledialog.askstring("Новый пользователь", "Введите имя:")
        if name and name not in self.users:
            self.users[name] = User(name)
            self.user_var.set(name)
            self.current_user = name
            self.update_display()
            self.user_combo['values'] = list(self.users.keys())
            self.update_display()


    def delete_user(self): #удаляет текущего пользователя
        if len(self.users) > 1 and self.current_user in self.users:
            del self.users[self.current_user]
            self.current_user = list(self.users.keys())[0]
            self.user_var.set(self.current_user)
            self.update_display()
	          self.user_combo['values'] = list(self.users.keys())
            self.update_display()


    def change_user(self, event): #смена текущего пользователя
        self.current_user = self.user_var.get()
        self.update_display()

    def add_transaction(self): #добавляет операцию
        try:
            #проверка суммы
            amount_text = self.amount_entry.get().strip()
            if not amount_text:
                messagebox.showerror("Ошибка", "Введите сумму.")
                return
            
            amount = float(amount_text)
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительной.")
                return
            
            #проверка описания
            description = self.desc_entry.get().strip()
            if not description:
                messagebox.showerror("Ошибка", "Введите описание.")
                return
            
            #проверка категории
            category = self.category_var.get().strip()
            if not category:
                messagebox.showerror("Ошибка", "Выберите категорию.")
                return
            
            trans_type = self.type_var.get()
            transaction = Expense(amount, description, category, trans_type)
            self.users[self.current_user].add_transaction(transaction)
            
            #jчистка полей и обновление интерфейса
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.update_display()
            messagebox.showinfo("Успех", "Операция добавлена.")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму.")

    def update_display(self): #обновляет интерфейс
        self.update_history()
        self.update_stats()

    def update_history(self): #обновляет таблицу истории операций
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        user = self.users[self.current_user]
        for transaction in user.get_transaction_history():
            date_str = transaction.date.strftime("%d.%m.%Y")
            amount_str = f"+{transaction.amount} руб." if transaction.transaction_type == "Доход" else f"-{transaction.amount} руб."
            
            self.history_tree.insert("", "end", values=(date_str, transaction.transaction_type.capitalize(),
                transaction.category, transaction.description, amount_str))

    def update_stats(self): #обновляет текст статистики
        user = self.users[self.current_user]
        stats = user.get_stats()
        
        stats_text = f"""ФИНАНСОВАЯ СТАТИСТИКА ({self.current_user})
        Доходы: {stats['income']:.2f} руб.
        Расходы: {stats['expenses']:.2f} руб.
        Баланс: {stats['balance']:.2f} руб."""
        
        if stats['income'] > 0:
            ratio = (stats['expenses'] / stats['income'] * 100) if stats['income'] > 0 else 0
            stats_text += f"\nСоотношение: {ratio:.1f}% расходов от доходов"

        #cтатистика по категориям расходов
        if stats['expense_categories']:
            stats_text += "\n\nРАСХОДЫ ПО КАТЕГОРИЯМ:\n"
            for category, total in stats['expense_categories'].items():
                percent = (total / stats['expenses'] * 100) if stats['expenses'] > 0 else 0
                stats_text += f"  {category}: {total:.2f} руб. ({percent:.1f}%)\n"

        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)

    def show_chart(self): #показывает график расходов по категориям
        user = self.users[self.current_user]
        stats = user.get_stats()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if stats['expense_categories']:
            categories = list(stats['expense_categories'].keys())
            amounts = list(stats['expense_categories'].values())
            
            ax.pie(amounts, labels=categories, autopct='%1.1f%%')
            ax.set_title('Расходы по категориям')
        else:
            ax.text(0.5, 0.5, 'Нет данных о расходах', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12)
            ax.set_title('Расходы по категориям')
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    import tkinter.simpledialog
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()

