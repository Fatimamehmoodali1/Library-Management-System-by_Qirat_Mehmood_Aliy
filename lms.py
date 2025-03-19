import json
from datetime import datetime, timedelta


class BookCollection:
    def __init__(self):
        self.book_list = []
        self.users = {}
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.storage_file, "r") as file:
                data = json.load(file)
                self.book_list = data.get("books", [])
                self.users = data.get("users", {})
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []
            self.users = {}

    def save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump({"books": self.book_list, "users": self.users}, file, indent=4)

    def create_new_book(self):
        book_title = input("Enter book title: ")
        book_author = input("Enter author: ")
        publication_year = input("Enter publication year: ")
        book_genre = input("Enter genre: ")
        is_book_read = input("Have you read this book? (yes/no): ").strip().lower() == "yes"
        rating = float(input("Rate the book (1-5): ")) if is_book_read else None
        review = input("Write a short review: ") if is_book_read else ""

        new_book = {
            "title": book_title,
            "author": book_author,
            "year": publication_year,
            "genre": book_genre,
            "read": is_book_read,
            "rating": rating,
            "review": review,
            "due_date": None,
        }

        self.book_list.append(new_book)
        self.save_to_file()
        print("Book added successfully!\n")

    def borrow_book(self):
        book_title = input("Enter the title of the book to borrow: ")
        username = input("Enter your username: ")
        due_date = datetime.now() + timedelta(days=14)

        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                book["due_date"] = due_date.strftime("%Y-%m-%d")
                self.users[username] = self.users.get(username, []) + [book_title]
                self.save_to_file()
                print(f"Book borrowed successfully! Due date: {book['due_date']}\n")
                return
        print("Book not found!\n")

    def return_book(self):
        book_title = input("Enter the title of the book to return: ")
        username = input("Enter your username: ")

        if username in self.users and book_title in self.users[username]:
            for book in self.book_list:
                if book["title"].lower() == book_title.lower():
                    due_date = datetime.strptime(book["due_date"], "%Y-%m-%d")
                    days_late = (datetime.now() - due_date).days
                    fine = max(0, days_late * 5)
                    book["due_date"] = None
                    self.users[username].remove(book_title)
                    if not self.users[username]:
                        del self.users[username]
                    self.save_to_file()
                    print(f"Book returned successfully! Fine: Rs.{fine}\n")
                    return
        print("Book not found or not borrowed by user!\n")

    def show_all_books(self):
        if not self.book_list:
            print("Your collection is empty.\n")
            return

        sort_option = input("Sort by (title/author/genre): ")
        self.book_list.sort(key=lambda x: x.get(sort_option, "").lower())

        print("Your Book Collection:")
        for index, book in enumerate(self.book_list, 1):
            reading_status = "Read" if book["read"] else "Unread"
            print(
                f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}"
            )
        print()

    def start_application(self):
        while True:
            print("📚 Welcome to Your Book Collection Manager! 📚")
            print("1. Add a new book")
            print("2. Borrow a book")
            print("3. Return a book")
            print("4. View all books")
            print("5. Exit")
            user_choice = input("Please choose an option (1-5): ")

            if user_choice == "1":
                self.create_new_book()
            elif user_choice == "2":
                self.borrow_book()
            elif user_choice == "3":
                self.return_book()
            elif user_choice == "4":
                self.show_all_books()
            elif user_choice == "5":
                self.save_to_file()
                print("Thank you for using Book Collection Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    book_manager = BookCollection()
    book_manager.start_application()




