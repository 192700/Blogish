# Blogish
# My Personal Blog
## Video Demo: 
[CS50 Final Project - My Personal Blog](https://youtu.be/dySuH8xAoV8)

![cs50-final-project](https://user-images.githubusercontent.com/55910194/139580203-018db37c-67da-4ddf-a497-baa9a33ef905.gif)
## Description: 

This project is a web application made using Python, Flask, HTML, TailwindCSS and MySQL. It is a blog site, where anyone can read blogs, write new blogs, update/edit existing blogs or delete any blog. 

## How to run this program?
**Prequisites**: Python3.8+, MySQL Server setup
**Steps to run**:
- Download or clone the source files. 
    - `git clone https://github.com/an4s911/cs50-final-project`
    - `cd cs50-final-project`
- Make a new file called `.env`
    - set the environment variables for MySQL
        - `MYSQL_USERNAME` & `MYSQL_PASSWORD`
    - set the secret key: a random byte value. You can do something like this
        - `SECRET_KEY=b'oap4kc73lcj'`
    - the `.env` file might look something like this
        ```
        MYSQL_USERNAME=testuser
        MYSQL_PASSWORD=testpass
        SECRET_KEY=b'oniw72js782a'
        ```
- Make a new virtual environment and source it.
    - `python -m venv venv`
    - For Windows:
        - `source venv\Scripts\activate`
    - For Unix-like:
        - `source venv/bin/activate`
- Install the requirements using `pip`
    - `pip install -r requirements.txt`
- Run the python app. 
    - `python app.py`
- Open `localhost:8000` in your browser. 

## The files in the project
### `app.py`
This is the main flask application. This is where all the routes and views are managed, the models are managed and also where all the errors and managed. 

This application is what runs the server. And handles all the `GET` requests and `POST` requests and renders or returns the necessary webpages and/or files.

### `tailwind.config.js`
This is a config file for the CSS framework **Tailwind**. Tailwind automatically generates the CSS, but the styles can modified or custmized using this config file.

### `styles.css`
This is the stylesheet generated by Tailwind CLI.

### A bunch of images. 
The numbered ones are images for HTTP error pages.

The `construction.jpg` is for pages that are currently not fully developed(or *under construction*)

The `logo.png` is the logo and `banner.jpg` is the banner.

The `archive.jpg` is the banner for the archive page.
```
400.png  404.png  410.png  429.png  503.png  archive.jpg  construction.jpg
403.png  405.png  418.png  500.png  504.png  banner.jpg   logo.png
```

### `archive.html`
This is template for the archive page where you can see all the blogs posts listed. It is extending to the `index.html` template.

### `base.html`
This is the base template on top of which every other template is rendered. Every other template is extended to this template. 

This is where the header, the banner, and the footer is. The theme of the site is all made here.

### `edit_post.html`
This is the template for editting the post. It is extending to the `new-post.html` template because they are very similar, with the difference that edit post will have some values in the input fields.

### `error.html`
This is the template that is rendered for any HTTP Status errors. Like 404, 405 etc. Extended to `base.html`.

### `index.html`
This the template for the home page of the site. This is extended to the `post_template.html` template. Why? Because there were multiple sites that had the same theme. 

This template only displays the 5 most recent posts (unlike the archive), shortened.

### `new-post.html`
This is the template for writing a new post. This is extended to the `post_template.html`.

This has a field for title, the content of the blog post, a checkbox for Drafting, and a post button to publish the blog post.

### `post_template.html`
This template is used for some of the pages in the site. It is extended to `base.html`.

It makes a section which is required in multiple other templates with CSS applied. The section is applied padding, margin, display property, background color et al. 

### `post.html`
This is the template for an individual post. It is extended to `post_template.html`. 

This shows the title, of the post and its content for users to read. Here we can select edit and also delete the post if needed. 