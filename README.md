# PyGramDownloader

![ProjectImage](https://github.com/muhfalihr/mystorage/blob/master/20240113_204134.jpg)

**Tool Description:**
PyGramDownloader is a sophisticated tool designed to facilitate users in downloading images and videos from user posts on the popular social media platform, Instagram. With an intuitive interface and powerful functionality, PyGramDownloader allows users to explore and save interesting content from Instagram accounts they admire.

Key Features of PyGramDownloader:

1. **Download Images and Videos:**
   PyGramDownloader enables users to download high-quality images and videos from Instagram user posts. With a single click, users can save compelling content to share with friends or keep for later viewing.

2. **User-Friendly Interface:**
   The PyGramDownloader user interface is designed to provide a seamless and easily understandable user experience. With simple navigation, users can quickly grasp how to use the tool without requiring in-depth technical knowledge.

3. **High-Quality Download Options:**
   PyGramDownloader provides users with the flexibility to choose the quality of images and videos they want to download. This allows users to save storage space and ensure that the downloaded content aligns with their preferences.

4. **Support for Various Instagram Accounts:**
   The tool supports downloads from various Instagram accounts, allowing users to explore and download content from friends, celebrities, or other popular accounts.

5. **Security and Privacy:**
   PyGramDownloader is implemented with a focus on user security and privacy. The tool does not require user login information, ensuring the security of users' Instagram accounts.

6. **Regular Updates:**
   To maintain availability and reliability, PyGramDownloader receives regular updates. This ensures that the tool can always adapt to the latest changes on the Instagram platform.

With PyGramDownloader, users can easily explore and collect their favorite content from Instagram, offering a fast, secure, and intuitive downloading experience.

## Requirements

- **Python**

  Already installed Python with version 3.10.12. See the [Installation and Setting up Python](https://github.com/muhfalihr/PyGramDownloader/?tab=readme-ov-file#installation-of-python-31012).

- **Have an active Instagram account**

  Used to run programs because cookies are required from that account. If you don't have a Instagram account, you have to [log in](https://www.instagram.com/accounts/login/) first.

## Clone the repository to your directory

```sh
# Change Directory
cd /home/ubuntu/Desktop

# Install gh
sudo apt install gh

# Auth gh
gh auth login

# Clonig Repository
gh repo clone muhfalihr/PyGramDownloader

# Change Directory
cd PyGramDownloader/
```

## Installation of Python 3.10.12

- Install Python version 3.

  ```sh
  apt install python3
  ```

- Instal Virtual environment for Python version 3.

  ```sh
  apt install python3-venv
  ```

- Create a Python virtual environment using the venv module.

  ```sh
  python3 -m venv .venv/my-venv
  ```

- Install the python package according to the requirements.txt file.

  ```sh
  .venv/my-venv/bin/pip install -r requirements.txt
  ```

## How to use ?

1. You need to give execute permission to the Python file. Use the following command in terminal or command prompt:

   ```sh
   chmod +x pgd
   ```

2. Add cookies to the cookie file to be created.

   ```sh
   ./pgd -cookie 'your-cookie'
   ```

3. Functions used in running the program. As follows :

   - **_Allmedia_**

     Downloads all media from a specific user's posts.

     ```sh
     ./pgd -func allmedia -un <user-name> -p /path/to/save
     ```

   - **_Images_**

     Downloads all images from the specified user's posts.

     ```sh
     ./pgd -func images -un <user-name> -p /path/to/save
     ```

### Description of the arguments used.

1. **_--function/-func_**

   Used to determine the name of the function that will execute the arguments entered.

2. **_--path/-p_**

   Used to specify the path of the folder to save the download results. The default is the default folder where the download results are saved, namely the **Downloads** folder.

3. **_--username/-un_**

   Used to determine the user name of the user whose media posts we will download.

4. **_--count/-count_**

   Used to determine the amount of media from user posts that will be downloaded. Even so, it won't affect anything because the response in the API is inconsistent. The default value is 33.

5. **_--max_id/-max_id_**

   Used to retrieve the next API response.

6. **_--version_**

   See the version for this PyGramDownloader tool.

7. **_--cookie/-cookie_**

   Used to enter your browser cookies.

## License

The PyGramDownloader project is licensed by [MIT License](https://github.com/muhfalihr/PyGramDownloader/blob/master/LICENSE).
