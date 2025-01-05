"""
File Name: Item_resurrected.py.py
Description: The program allows adding information about items 
    (item name, item description, contact information), deleting 
    item information, displaying a list of items, and also allowing 
    to find information about items
Author: Zhou Wanyao
Date: 2024-12-26

"""
import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

# 1. 定义 User 类
class User:
    # 静态变量，用于生成用户ID，起始为100000000
    current_id = 100000000

    def __init__(self, name, address, phone, email, user_id=None, password="user123", role="user", is_verified=False):
        # 如果没有提供user_id，则自动分配一个新的ID
        if user_id is None:
            self.user_id = User.current_id
            User.current_id += 1  # 每创建一个用户，ID增加
        else:
            self.user_id = user_id
            # 确保current_id更新到下一个未使用的ID
            if user_id >= User.current_id:
                User.current_id = user_id + 1
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.role = role  # 'user' 或 'admin'
        self.is_verified = is_verified

    def register(self):
        """返回用户的注册信息"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'is_verified': self.is_verified
        }

    def verify(self):
        """管理员审核用户，标记为已审核"""
        self.is_verified = True

    def set_password(self, password):
        """管理员可以修改用户的密码"""
        self.password = password

    def check_password(self, password):
        """检查密码是否匹配"""
        return self.password == password

    def save_to_file(self):
        """保存用户信息到文件"""
        user_info = self.register()
        with open("users_info.txt", "a", encoding='utf-8') as f:
            f.write(json.dumps(user_info, ensure_ascii=False) + "\n")

    @staticmethod
    def load_users():
        """从文件加载用户信息"""
        users = {}
        if os.path.exists("users_info.txt"):
            with open("users_info.txt", "r", encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        user_info = json.loads(line.strip())
                        if user_info['role'] == 'admin':
                            user = Admin(
                                user_id=user_info['user_id'],
                                name=user_info['name'],
                                address=user_info['address'],
                                phone=user_info['phone'],
                                email=user_info['email'],
                                password=user_info['password']
                            )
                        else:
                            user = User(
                                name=user_info['name'],
                                address=user_info['address'],
                                phone=user_info['phone'],
                                email=user_info['email'],
                                user_id=user_info['user_id'],
                                password=user_info['password'],
                                role=user_info['role'],
                                is_verified=user_info['is_verified']
                            )
                        users[user.user_id] = user
                        # 更新current_id确保唯一性
                        if user.user_id >= User.current_id:
                            User.current_id = user.user_id + 1
        return users

# 2. 定义 Admin 类，继承 User 类
class Admin(User):
    def __init__(self, user_id, name, address, phone, email, password="admin123"):
        # 调用父类的构造函数
        super().__init__(name, address, phone, email, user_id=user_id, password=password, role="admin", is_verified=True)

    def add_item_type(self, type_name, attributes):
        """管理员新增物品类型"""
        ItemCategory.add_category(type_name, attributes)

    def delete_item_type(self, type_name):
        """管理员删除物品类型"""
        ItemCategory.delete_category(type_name)

    def modify_item_type(self, type_name, attributes):
        """管理员修改物品类型"""
        ItemCategory.modify_category(type_name, attributes)

    def view_pending_users(self, users):
        """管理员查看所有待审核的用户"""
        return [user for user in users.values() if not user.is_verified and user.role != "admin"]

    def approve_user(self, user):
        """管理员审核通过某个用户"""
        if user.is_verified:
            return f"用户 {user.name} 已审核通过。"
        user.verify()
        return f"用户 {user.name} 已审核通过。"

    def reset_user_password(self, user, new_password):
        """管理员重置用户密码"""
        user.set_password(new_password)
        return f"用户 {user.name} 的密码已重置为 '{new_password}'。"

# 3. 定义 Item 和 ItemCategory 类
class Item:
    items = []

    @classmethod
    def load_items(cls, users):
        """从文件加载物品信息"""
        if os.path.exists("items.txt"):
            with open("items.txt", "r", encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        item_info = json.loads(line.strip())
                        owner_id = item_info['owner_id']
                        owner = users.get(owner_id)
                        if owner:
                            item = Item(
                                name=item_info['name'],
                                description=item_info['description'],
                                category=item_info['category'],
                                owner=owner
                            )
                            cls.items.append(item)

    @classmethod
    def save_items(cls):
        """将所有物品信息保存到文件"""
        with open("items.txt", "w", encoding='utf-8') as f:
            for item in cls.items:
                item_info = {
                    'name': item.name,
                    'description': item.description,
                    'category': item.category,
                    'owner_id': item.owner.user_id
                }
                f.write(json.dumps(item_info, ensure_ascii=False) + "\n")

    @classmethod
    def add_item(cls, name, description, category, owner):
        new_item = Item(name, description, category, owner)
        cls.items.append(new_item)
        cls.save_items()

    @classmethod
    def search_item(cls, category, keyword):
        """根据类别和关键字搜索物品"""
        return [item for item in cls.items if category in item.category and (keyword.lower() in item.name.lower() or keyword.lower() in item.description.lower())]

    @classmethod
    def delete_item(cls, item):
        """删除物品"""
        if item in cls.items:
            cls.items.remove(item)
            cls.save_items()
            return f"物品 '{item.name}' 已删除。"
        return f"物品 '{item.name}' 不存在。"

    def __init__(self, name, description, category, owner):
        self.name = name
        self.description = description
        self.category = category
        self.owner = owner

class ItemCategory:
    categories = {}

    @staticmethod
    def load_categories():
        """加载物品类别，如果文件存在"""
        if os.path.exists("categories.txt"):
            with open("categories.txt", "r", encoding="utf-8") as file:
                for line in file:
                    if line.strip():
                        parts = line.strip().split(",", 1)
                        if len(parts) == 2:
                            name, description = parts
                            ItemCategory.add_category(name, {"描述": description}, save=False)

    @staticmethod
    def save_categories():
        """保存所有物品类别到文件"""
        with open("categories.txt", "w", encoding="utf-8") as file:
            for name, info in ItemCategory.categories.items():
                # 确保 info 是字典，并包含 '描述' 键
                if isinstance(info, dict) and '描述' in info:
                    file.write(f"{name},{info['描述']}\n")
                else:
                    print(f"警告: 类别 {name} 的数据格式不正确")

    @staticmethod
    def add_category(name, description, save=True):
        """添加物品类别"""
        ItemCategory.categories[name] = description
        if save:
            ItemCategory.save_categories()
        # messagebox.showinfo("添加成功", f"物品类别 '{name}' 已添加。")

    @staticmethod
    def delete_category(name, save=True):
        """删除物品类别"""
        if name in ItemCategory.categories:
            del ItemCategory.categories[name]
            if save:
                ItemCategory.save_categories()
            messagebox.showinfo("删除成功", f"物品类别 '{name}' 已删除。")
        else:
            messagebox.showerror("错误", f"物品类别 '{name}' 不存在。")

    @staticmethod
    def modify_category(name, new_description, save=True):
        """修改物品类别"""
        if name in ItemCategory.categories:
            ItemCategory.categories[name] = {"描述": new_description}
            if save:
                ItemCategory.save_categories()
            messagebox.showinfo("修改成功", f"物品类别 '{name}' 已修改。")
        else:
            messagebox.showerror("错误", f"物品类别 '{name}' 不存在。")

    @staticmethod
    def get_categories():
        """获取所有物品类别"""
        return ItemCategory.categories

# 4. 定义 Application 类，包含GUI逻辑
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("物品复活系统")
        self.geometry("900x700")

        # 加载用户信息
        self.users = User.load_users()

        # 确保Admin存在，如果没有，则创建一个
        if 1 not in self.users:
            admin = Admin(1, "管理员", "Admin Street", "1234567890", "admin@admin.com")
            self.users[admin.user_id] = admin
            admin.save_to_file()

        # 加载物品类别
        ItemCategory.load_categories()

        # 加载物品信息
        Item.load_items(self.users)

        self.current_user = None

        self.create_widgets()

    def create_widgets(self):
        # 主内容框架
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # 顶部标签
        self.label = tk.Label(self.main_frame, text="物品复活系统", font=("Arial", 24))
        self.label.pack(pady=20)

        # 功能按钮框架
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=10)

        # 添加物品按钮（普通用户）
        self.add_item_button = tk.Button(self.buttons_frame, text="添加物品", command=self.add_item, state=tk.DISABLED)
        self.add_item_button.grid(row=0, column=0, padx=5, pady=5)

        # 修改物品按钮（普通用户）
        self.modify_item_button = tk.Button(self.buttons_frame, text="修改物品", command=self.modify_item, state=tk.DISABLED)
        self.modify_item_button.grid(row=0, column=1, padx=5, pady=5)

        # 搜索物品按钮（普通用户）
        self.search_item_button = tk.Button(self.buttons_frame, text="搜索物品", command=self.search_item, state=tk.DISABLED)
        self.search_item_button.grid(row=0, column=2, padx=5, pady=5)

        # 删除物品按钮（普通用户）
        self.delete_item_button = tk.Button(self.buttons_frame, text="删除物品", command=self.delete_item, state=tk.DISABLED)
        self.delete_item_button.grid(row=0, column=3, padx=5, pady=5)

        # 显示全部物品按钮（管理员）
        self.view_all_items_button = tk.Button(self.buttons_frame, text="显示全部物品", command=self.view_all_items, state=tk.DISABLED)
        self.view_all_items_button.grid(row=0, column=4, padx=5, pady=5)

        # 审核待审核用户按钮（管理员）
        self.view_pending_users_button = tk.Button(self.buttons_frame, text="审核待审核用户", command=self.view_pending_users, state=tk.DISABLED)
        self.view_pending_users_button.grid(row=0, column=5, padx=5, pady=5)

        # 管理物品类别按钮（管理员）
        self.manage_categories_button = tk.Button(self.buttons_frame, text="管理物品类别", command=self.manage_categories, state=tk.DISABLED)
        self.manage_categories_button.grid(row=0, column=6, padx=5, pady=5)

        # 重置密码按钮（管理员）
        self.reset_password_button = tk.Button(self.buttons_frame, text="重置用户密码", command=self.reset_user_password, state=tk.DISABLED)
        self.reset_password_button.grid(row=0, column=7, padx=5, pady=5)

        # 注册按钮
        self.register_button = tk.Button(self.main_frame, text="注册", command=self.open_register_window)
        self.register_button.pack(pady=10)

        # 注销按钮
        self.logout_button = tk.Button(self.main_frame, text="注销", command=self.logout, state=tk.DISABLED)
        self.logout_button.pack(pady=10)

        # 登录框架（始终在底部）
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(side="bottom", fill="x", pady=20)

        self.login_user_id_label = tk.Label(self.login_frame, text="用户ID:")
        self.login_user_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.login_user_id_entry = tk.Entry(self.login_frame)
        self.login_user_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.login_password_label = tk.Label(self.login_frame, text="密码:")
        self.login_password_label.grid(row=1, column=0, padx=5, pady=5)
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tk.Button(self.login_frame, text="登录", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def open_register_window(self):
        """打开注册窗口"""
        register_window = tk.Toplevel(self)
        register_window.title("用户注册")
        register_window.geometry("400x350")

        tk.Label(register_window, text="姓名:").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(register_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(register_window, text="地址:").grid(row=1, column=0, padx=10, pady=10)
        address_entry = tk.Entry(register_window)
        address_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(register_window, text="电话:").grid(row=2, column=0, padx=10, pady=10)
        phone_entry = tk.Entry(register_window)
        phone_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(register_window, text="邮箱:").grid(row=3, column=0, padx=10, pady=10)
        email_entry = tk.Entry(register_window)
        email_entry.grid(row=3, column=1, padx=10, pady=10)

        submit_button = tk.Button(register_window, text="提交注册",
                                  command=lambda: self.register_user(register_window, name_entry.get(),
                                                                   address_entry.get(),
                                                                   phone_entry.get(),
                                                                   email_entry.get()))
        submit_button.grid(row=4, column=0, columnspan=2, pady=20)

    def register_user(self, register_window, name, address, phone, email):
        """提交用户注册信息"""
        if not all([name, address, phone, email]):
            messagebox.showerror("错误", "所有字段均为必填项。")
            return

        # 创建用户并保存
        user = User(name, address, phone, email)
        self.users[user.user_id] = user

        # 将用户信息保存到文件
        user.save_to_file()

        messagebox.showinfo("注册成功", f"{name} 注册成功！\n您的用户ID是 {user.user_id}\n初始密码是 'user123'，请等待管理员审核。")
        register_window.destroy()

    def login(self):
        """用户登录"""
        user_id = self.login_user_id_entry.get()
        password = self.login_password_entry.get()

        if not user_id.isdigit():
            messagebox.showerror("登录失败", "用户ID必须是数字。")
            return

        user_id = int(user_id)
        user = self.users.get(user_id)

        if user:
            if user.check_password(password):
                if user.role == "admin":
                    self.current_user = user
                    messagebox.showinfo("登录成功", f"管理员 {user.name} 登录成功！")
                else:
                    if user.is_verified:
                        self.current_user = user
                        messagebox.showinfo("登录成功", f"{user.name} 登录成功！")
                    else:
                        messagebox.showwarning("未审核", "您的账户尚未通过管理员审核。")
                        return
                self.enable_user_buttons()
            else:
                messagebox.showerror("登录失败", "密码错误。")
        else:
            messagebox.showerror("登录失败", "无效的用户ID。")

    def enable_user_buttons(self):
        """根据当前用户角色启用按钮"""
        self.add_item_button.config(state=tk.NORMAL)
        self.modify_item_button.config(state=tk.NORMAL)
        self.search_item_button.config(state=tk.NORMAL)
        self.delete_item_button.config(state=tk.NORMAL)
        self.logout_button.config(state=tk.NORMAL)

        if self.current_user.role == "admin":
            self.view_pending_users_button.config(state=tk.NORMAL)
            self.manage_categories_button.config(state=tk.NORMAL)
            self.reset_password_button.config(state=tk.NORMAL)
            self.view_all_items_button.config(state=tk.NORMAL)
        else:
            self.view_pending_users_button.config(state=tk.DISABLED)
            self.manage_categories_button.config(state=tk.DISABLED)
            self.reset_password_button.config(state=tk.DISABLED)
            self.view_all_items_button.config(state=tk.DISABLED)

        # 禁用登录按钮和注册按钮
        self.login_button.config(state=tk.DISABLED)
        self.register_button.config(state=tk.DISABLED)

    def logout(self):
        """注销当前用户，返回登录界面"""
        self.current_user = None
        self.add_item_button.config(state=tk.DISABLED)
        self.modify_item_button.config(state=tk.DISABLED)
        self.search_item_button.config(state=tk.DISABLED)
        self.delete_item_button.config(state=tk.DISABLED)
        self.view_pending_users_button.config(state=tk.DISABLED)
        self.manage_categories_button.config(state=tk.DISABLED)
        self.reset_password_button.config(state=tk.DISABLED)
        self.view_all_items_button.config(state=tk.DISABLED)
        self.logout_button.config(state=tk.DISABLED)

        # 启用登录按钮和注册按钮
        self.login_button.config(state=tk.NORMAL)
        self.register_button.config(state=tk.NORMAL)

        # 清空登录框
        self.login_user_id_entry.delete(0, tk.END)
        self.login_password_entry.delete(0, tk.END)

        messagebox.showinfo("注销", "已成功注销当前用户。")

    def view_pending_users(self):
        """显示所有待审核的用户并允许管理员审核"""
        if isinstance(self.current_user, Admin):
            pending_users = self.current_user.view_pending_users(self.users)
            if not pending_users:
                messagebox.showinfo("无待审核用户", "没有待审核的用户。")
                return

            pending_window = tk.Toplevel(self)
            pending_window.title("待审核用户")
            pending_window.geometry("600x400")

            tk.Label(pending_window, text="待审核用户列表", font=("Arial", 16)).pack(pady=10)

            canvas = tk.Canvas(pending_window)
            scrollbar = tk.Scrollbar(pending_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for user in pending_users:
                frame = tk.Frame(scrollable_frame, borderwidth=1, relief="solid", padx=10, pady=10)
                frame.pack(padx=10, pady=5, fill="x")

                info = f"用户ID: {user.user_id}\n姓名: {user.name}\n地址: {user.address}\n电话: {user.phone}\n邮箱: {user.email}"
                tk.Label(frame, text=info, justify="left").pack(side="left")

                approve_button = tk.Button(frame, text="审核通过", command=lambda u=user, w=pending_window: self.approve_user(u, w))
                approve_button.pack(side="right")

        else:
            messagebox.showerror("权限不足", "只有管理员才能查看待审核用户。")

    def approve_user(self, user, pending_window):
        """管理员审核通过用户"""
        if isinstance(self.current_user, Admin):
            approval_message = self.current_user.approve_user(user)
            # 更新用户信息到文件
            self.save_all_users()
            messagebox.showinfo("用户审核", approval_message)
            pending_window.destroy()
        else:
            messagebox.showerror("权限不足", "您没有权限审核用户。")

    def manage_categories(self):
        """管理物品类别"""
        if not isinstance(self.current_user, Admin):
            messagebox.showerror("权限不足", "只有管理员才能管理物品类别。")
            return

        manage_window = tk.Toplevel(self)
        manage_window.title("管理物品类别")
        manage_window.geometry("500x400")

        tk.Label(manage_window, text="物品类别列表", font=("Arial", 16)).pack(pady=10)

        listbox = tk.Listbox(manage_window, width=50)
        listbox.pack(pady=10)

        for category in ItemCategory.categories:
            listbox.insert(tk.END, category)

        # 按钮框架
        buttons_frame = tk.Frame(manage_window)
        buttons_frame.pack(pady=10)

        add_button = tk.Button(buttons_frame, text="添加类别", command=lambda: self.add_category(listbox))
        add_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(buttons_frame, text="删除类别", command=lambda: self.delete_category(listbox))
        delete_button.grid(row=0, column=1, padx=5)

        modify_button = tk.Button(buttons_frame, text="修改类别", command=lambda: self.modify_category(listbox))
        modify_button.grid(row=0, column=2, padx=5)

    def add_category(self, listbox):
        """添加物品类别"""
        type_name = simpledialog.askstring("添加类别", "请输入物品类别名称：")
        if type_name:
            if type_name in ItemCategory.categories:
                messagebox.showerror("错误", "该类别已存在。")
                return
            attributes = simpledialog.askstring("添加类别", "请输入类别描述：")
            if not attributes:
                messagebox.showerror("错误", "类别描述不能为空。")
                return
            ItemCategory.add_category(type_name, attributes)
            listbox.insert(tk.END, type_name)

    def delete_category(self, listbox):
        """删除物品类别"""
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("错误", "请选择要删除的类别。")
            return
        type_name = listbox.get(selected[0])
        confirmation = messagebox.askyesno("确认删除", f"是否删除类别 '{type_name}'？")
        if confirmation:
            ItemCategory.delete_category(type_name)
            listbox.delete(selected[0])

    def modify_category(self, listbox):
        """修改物品类别"""
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("错误", "请选择要修改的类别。")
            return
        type_name = listbox.get(selected[0])
        new_attributes = simpledialog.askstring("修改类别", f"请输入类别 '{type_name}' 的新描述：")
        if new_attributes:
            ItemCategory.modify_category(type_name, new_attributes)

    def add_item(self):
        """添加物品"""
        add_window = tk.Toplevel(self)
        add_window.title("添加物品")
        add_window.geometry("400x400")

        tk.Label(add_window, text="物品名称:").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_window, text="物品描述:").grid(row=1, column=0, padx=10, pady=10)
        description_entry = tk.Entry(add_window)
        description_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(add_window, text="物品类别:").grid(row=2, column=0, padx=10, pady=10)
        category_var = tk.StringVar(add_window)
        categories = list(ItemCategory.categories.keys())
        if categories:
            category_var.set(categories[0])
            category_menu = tk.OptionMenu(add_window, category_var, *categories)
        else:
            category_var.set("无类别")
            category_menu = tk.OptionMenu(add_window, category_var, "无类别")
            category_menu.config(state=tk.DISABLED)
            messagebox.showwarning("警告", "当前没有物品类别，请联系管理员添加类别后再添加物品。")
        category_menu.grid(row=2, column=1, padx=10, pady=10)

        submit_button = tk.Button(add_window, text="添加",
                                  command=lambda: self.submit_add_item(add_window, name_entry.get(),
                                                                    description_entry.get(),
                                                                    category_var.get()))
        submit_button.grid(row=3, column=0, columnspan=2, pady=20)

    def submit_add_item(self, window, name, description, category):
        """提交添加物品信息"""
        if category == "无类别" or category == "选择类别":
            messagebox.showerror("错误", "请选择物品类别。")
            return
        if not all([name, description, category]):
            messagebox.showerror("错误", "所有字段均为必填项。")
            return

        Item.add_item(name, description, category, self.current_user)
        messagebox.showinfo("成功", f"物品 '{name}' 添加成功。")
        window.destroy()

    def modify_item(self):
        """修改物品"""
        modify_window = tk.Toplevel(self)
        modify_window.title("修改物品")
        modify_window.geometry("600x400")

        user_items = [item for item in Item.items if item.owner.user_id == self.current_user.user_id]
        if not user_items:
            messagebox.showinfo("无物品", "您尚未添加任何物品。")
            modify_window.destroy()
            return

        tk.Label(modify_window, text="选择要修改的物品:").pack(pady=10)

        selected_item = tk.StringVar(modify_window)
        selected_item.set(user_items[0].name)

        item_menu = tk.OptionMenu(modify_window, selected_item, *[item.name for item in user_items])
        item_menu.pack(pady=5)

        tk.Label(modify_window, text="新物品名称:").pack(pady=5)
        new_name_entry = tk.Entry(modify_window)
        new_name_entry.pack(pady=5)

        tk.Label(modify_window, text="新物品描述:").pack(pady=5)
        new_description_entry = tk.Entry(modify_window)
        new_description_entry.pack(pady=5)

        submit_button = tk.Button(modify_window, text="修改",
                                  command=lambda: self.submit_modify_item(modify_window, selected_item.get(),
                                                                        new_name_entry.get(),
                                                                        new_description_entry.get()))
        submit_button.pack(pady=20)

    def submit_modify_item(self, window, old_name, new_name, new_description):
        """提交修改物品信息"""
        if not all([new_name, new_description]):
            messagebox.showerror("错误", "所有字段均为必填项。")
            return

        # 找到对应的物品
        item = next((item for item in Item.items if item.name == old_name and item.owner.user_id == self.current_user.user_id), None)
        if item:
            item.name = new_name
            item.description = new_description
            Item.save_items()
            messagebox.showinfo("成功", f"物品 '{old_name}' 已修改为 '{new_name}'。")
            window.destroy()
        else:
            messagebox.showerror("错误", "未找到指定物品。")

    def search_item(self):
        """搜索物品"""
        search_window = tk.Toplevel(self)
        search_window.title("搜索物品")
        search_window.geometry("400x300")

        tk.Label(search_window, text="物品类别:").grid(row=0, column=0, padx=10, pady=10)
        category_var = tk.StringVar(search_window)
        category_var.set("选择类别")
        category_menu = tk.OptionMenu(search_window, category_var, *ItemCategory.categories.keys())
        category_menu.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(search_window, text="关键词:").grid(row=1, column=0, padx=10, pady=10)
        keyword_entry = tk.Entry(search_window)
        keyword_entry.grid(row=1, column=1, padx=10, pady=10)

        submit_button = tk.Button(search_window, text="搜索",
                                  command=lambda: self.submit_search_item(search_window, category_var.get(),
                                                                        keyword_entry.get()))
        submit_button.grid(row=2, column=0, columnspan=2, pady=20)

    def submit_search_item(self, window, category, keyword):
        """提交搜索物品信息"""
        if category == "选择类别":
            messagebox.showerror("错误", "请选择物品类别。")
            return
        if not keyword:
            messagebox.showerror("错误", "关键词不能为空。")
            return

        results = Item.search_item(category, keyword)
        if results:
            result_text = "\n\n".join([f"名称: {item.name}\n描述: {item.description}\n所有者: {item.owner.name}" for item in results])
            messagebox.showinfo("搜索结果", result_text)
        else:
            messagebox.showinfo("无结果", "未找到符合条件的物品。")
        window.destroy()

    def delete_item(self):
        """删除物品"""
        delete_window = tk.Toplevel(self)
        delete_window.title("删除物品")
        delete_window.geometry("400x300")

        user_items = [item for item in Item.items if item.owner.user_id == self.current_user.user_id]
        if not user_items:
            messagebox.showinfo("无物品", "您尚未添加任何物品。")
            delete_window.destroy()
            return

        tk.Label(delete_window, text="选择要删除的物品:").pack(pady=10)

        selected_item = tk.StringVar(delete_window)
        selected_item.set(user_items[0].name)

        item_menu = tk.OptionMenu(delete_window, selected_item, *[item.name for item in user_items])
        item_menu.pack(pady=5)

        submit_button = tk.Button(delete_window, text="删除",
                                  command=lambda: self.submit_delete_item(delete_window, selected_item.get()))
        submit_button.pack(pady=20)

    def submit_delete_item(self, window, item_name):
        """提交删除物品信息"""
        item = next((item for item in Item.items if item.name == item_name and item.owner.user_id == self.current_user.user_id), None)
        if item:
            confirmation = messagebox.askyesno("确认删除", f"是否删除物品 '{item.name}'？")
            if confirmation:
                result = Item.delete_item(item)
                messagebox.showinfo("删除结果", result)
                window.destroy()
        else:
            messagebox.showerror("错误", "未找到指定物品。")

    def view_all_items(self):
        """显示全部物品列表"""
        if not isinstance(self.current_user, Admin):
            messagebox.showerror("权限不足", "只有管理员才能查看全部物品。")
            return

        view_window = tk.Toplevel(self)
        view_window.title("全部物品列表")
        view_window.geometry("700x500")

        tk.Label(view_window, text="全部物品列表", font=("Arial", 16)).pack(pady=10)

        canvas = tk.Canvas(view_window)
        scrollbar = tk.Scrollbar(view_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for item in Item.items:
            frame = tk.Frame(scrollable_frame, borderwidth=1, relief="solid", padx=10, pady=10)
            frame.pack(padx=10, pady=5, fill="x")

            info = f"名称: {item.name}\n描述: {item.description}\n类别: {item.category}\n所有者: {item.owner.name}"
            tk.Label(frame, text=info, justify="left").pack(side="left")

    def reset_user_password(self):
        """管理员重置用户密码"""
        reset_window = tk.Toplevel(self)
        reset_window.title("重置用户密码")
        reset_window.geometry("400x300")

        tk.Label(reset_window, text="选择用户:").pack(pady=10)

        # 获取所有用户（除管理员）
        users_list = [user for user in self.users.values() if user.role != "admin"]
        if not users_list:
            messagebox.showinfo("无用户", "当前没有普通用户。")
            reset_window.destroy()
            return

        selected_user = tk.StringVar(reset_window)
        selected_user.set(users_list[0].name)

        user_menu = tk.OptionMenu(reset_window, selected_user, *[user.name for user in users_list])
        user_menu.pack(pady=5)

        tk.Label(reset_window, text="新密码:").pack(pady=5)
        new_password_entry = tk.Entry(reset_window, show="*")
        new_password_entry.pack(pady=5)

        submit_button = tk.Button(reset_window, text="重置密码",
                                  command=lambda: self.submit_reset_password(reset_window, selected_user.get(),
                                                                            new_password_entry.get()))
        submit_button.pack(pady=20)

    def submit_reset_password(self, window, user_name, new_password):
        """提交重置密码信息"""
        if not new_password:
            messagebox.showerror("错误", "新密码不能为空。")
            return

        # 找到对应的用户
        user = next((user for user in self.users.values() if user.name == user_name and user.role != "admin"), None)
        if user:
            confirmation = messagebox.askyesno("确认重置", f"是否将用户 '{user.name}' 的密码重置为 '{new_password}'？")
            if confirmation:
                result = self.current_user.reset_user_password(user, new_password)
                self.save_all_users()
                messagebox.showinfo("重置成功", result)
                window.destroy()
        else:
            messagebox.showerror("错误", "未找到指定用户。")

    def view_all_items(self):
        """显示全部物品列表"""
        if not isinstance(self.current_user, Admin):
            messagebox.showerror("权限不足", "只有管理员才能查看全部物品。")
            return

        view_window = tk.Toplevel(self)
        view_window.title("全部物品列表")
        view_window.geometry("700x500")

        tk.Label(view_window, text="全部物品列表", font=("Arial", 16)).pack(pady=10)

        canvas = tk.Canvas(view_window)
        scrollbar = tk.Scrollbar(view_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for item in Item.items:
            frame = tk.Frame(scrollable_frame, borderwidth=1, relief="solid", padx=10, pady=10)
            frame.pack(padx=10, pady=5, fill="x")

            info = f"名称: {item.name}\n描述: {item.description}\n类别: {item.category}\n所有者: {item.owner.name}"
            tk.Label(frame, text=info, justify="left").pack(side="left")

    def save_all_users(self):
        """保存所有用户信息到文件"""
        with open("users_info.txt", "w", encoding='utf-8') as f:
            for user in self.users.values():
                f.write(json.dumps(user.register(), ensure_ascii=False) + "\n")

    def on_closing(self):
        """在关闭应用时保存所有用户信息和物品信息"""
        self.save_all_users()
        Item.save_items()
        self.destroy()

# 5. 主程序
if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # 确保关闭时保存数据
    app.mainloop()
