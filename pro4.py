# === Auto-install required packages ===
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from instagrapi import Client
except ImportError:
    install("instagrapi")
    from instagrapi import Client

try:
    import customtkinter as ctk
except ImportError:
    install("customtkinter")
    import customtkinter as ctk

import time
from instagrapi.exceptions import PrivateAccount
# === GUI Login Window ===
def show_login_window():   # This function creates the login screen.
    def attempt_login():
        user = username_entry.get()
        pwd = password_entry.get()
        try:
            cl.login(user, pwd)
            status_label.configure(text="✅ Login successful!", text_color="green")
            root.after(500, lambda: [root.destroy(), show_main_menu()])
           # Wait 500 milliseconds.and lambda is  anonymous function() Closes the login window)
        except Exception as e:
            status_label.configure(text=f"❌ Login failed: {e}", text_color="red")
# background color, size used configure and status lables show if login or feild
    ctk.set_appearance_mode("light") #overall look of the app to the light mode
    ctk.set_default_color_theme("blue") # buttons colours

    global root, username_entry, password_entry, status_label, cl
    #root The main login window of the GUI.username_entry	Field for entering Instagram username status lables show
    #it login succusfull or not
    cl = Client()
    root = ctk.CTk()
    root.geometry("400x350")
    root.title("Instagram Login")

    ctk.CTkLabel(master=root, text="Login to Instagram", font=("Segoe UI", 24, "bold")).pack(pady=20)
    username_entry = ctk.CTkEntry(master=root, placeholder_text="Username", width=250)
    username_entry.pack(pady=10)
    password_entry = ctk.CTkEntry(master=root, placeholder_text="Password", show="*", width=250)
    password_entry.pack(pady=10)
    ctk.CTkButton(master=root, text="Login", command=attempt_login, width=200).pack(pady=15)
    status_label = ctk.CTkLabel(master=root, text="")
    status_label.pack(pady=5)

    root.mainloop()

# === Username Check ===
def check_username_exists(cl, username):
    try:
        cl.user_id_from_username(username)
        return True
    except Exception:
        return False

# === Main Menu GUI ===
def show_main_menu():
    def follow_user():
        target = username_entry_box.get() #This line creates an input field to cheak username
        if check_username_exists(cl, target):
            user_id = cl.user_id_from_username(target)
            cl.user_follow(user_id)
            result_label.configure(text=f"✅ Followed {target}", text_color="green")
        else:
            result_label.configure(text="❌ Invalid username", text_color="red")
#cl is an instance of the Client() class from the instagrapi library 
#It handles all communication with Instagram (login, follow, like, etc.).
#Passing cl allows the function to use it for API calls.
    def unfollow_user():
        target = username_entry_box.get()
        if check_username_exists(cl, target):
            user_id = cl.user_id_from_username(target)
            my_user_id = cl.user_id_from_username(cl.username)
            following = cl.user_following(my_user_id)
            if user_id in following:
                cl.user_unfollow(user_id)
                result_label.configure(text=f"✅ Unfollowed {target}", text_color="green")
            else:
                result_label.configure(text=f"⚠️ You are not following {target}", text_color="orange")
        else:
            result_label.configure(text="❌ Invalid username", text_color="red")

    def like_user_posts():
        target = username_entry_box.get()
        if check_username_exists(cl, target):
            try:
                count = int(post_count_entry.get())
                user_id = cl.user_id_from_username(target)
                try:
                    medias = cl.user_medias(user_id, count)
                except PrivateAccount:
                    result_label.configure(text="⚠️ Cannot access posts — account may be private", text_color="orange")
                    return
                if medias:
                    for media in medias:
                        cl.media_like(media.id)
                        result_label.configure(text=f"❤️ Liked post ID: {media.id}", text_color="green")
                        root.update()
                        time.sleep(2)
                    result_label.configure(text=f"✅ Task done! {len(medias)} posts liked.", text_color="blue")
                else:
                    result_label.configure(text="⚠️ No posts found or account is private", text_color="orange")
            except ValueError:
                result_label.configure(text="❌ Enter a valid number of posts", text_color="red")
        else:
            result_label.configure(text="❌ Invalid username", text_color="red")

    def comment_on_post():
        target = username_entry_box.get()
        if check_username_exists(cl, target):
            try:
                user_id = cl.user_id_from_username(target)
                medias = cl.user_medias(user_id, 1)
                if medias:
                    comment = comment_entry.get()
                    cl.media_comment(medias[0].id, comment)
                    result_label.configure(text="💬 Comment added!", text_color="green")
                else:
                    result_label.configure(text="⚠️ No posts found or account is private", text_color="orange")
            except Exception as e:
                result_label.configure(text=f"⚠️ Error: {e}", text_color="orange")
        else:
            result_label.configure(text="❌ Invalid username", text_color="red")

    root = ctk.CTk()
    root.geometry("600x500")
    root.title("Instagram Bot GUI")

 #  ctk.CTkLabel(master=root, text="Instagram Bot GUI", font=("Segoe UI", 24, "bold")).pack(pady=20)
    ctk.CTkLabel(master=root, text="Welcome to insta bot", font=("Segoe UI", 24, "bold")).pack(pady=20)

    username_entry_box = ctk.CTkEntry(master=root, placeholder_text="Target Username", width=300)
    username_entry_box.pack(pady=5)

    post_count_entry = ctk.CTkEntry(master=root, placeholder_text="Number of posts to like", width=300)
    post_count_entry.pack(pady=5)

    comment_entry = ctk.CTkEntry(master=root, placeholder_text="Comment text", width=300)
    comment_entry.pack(pady=5)

    ctk.CTkButton(master=root, text="Follow", command=follow_user).pack(pady=8) #create follow button
    ctk.CTkButton(master=root, text="Unfollow", command=unfollow_user).pack(pady=8)
    ctk.CTkButton(master=root, text="Like Posts", command=like_user_posts).pack(pady=8)
    ctk.CTkButton(master=root, text="Comment", command=comment_on_post).pack(pady=8)

    result_label = ctk.CTkLabel(master=root, text="")
    result_label.pack(pady=15)

    ctk.CTkButton(master=root, text="Exit", command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_login_window()
