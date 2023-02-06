<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">xkcd downloader</h3>

  <p align="center">
    A Python script that downloads xkcd vignettes along with their explanation
    <br />
    <a href="https://github.com/HenestrosaConH/xkcd-downloader/issues">Report Bug</a> · <a href="https://github.com/HenestrosaConH/xkcd-downloader/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
   <summary>Table of Contents</summary>
   <ol>
      <li>
         <a href="#about-the-project">About The Project</a>
         <ul>
            <li><a href="#intended-usage">Intended Usage</a></li>
            <li><a href="#project-structure">Project Structure</a></li>
            <li><a href="#built-with">Built With</a></li>
         </ul>
      </li>
      <li>
         <a href="#getting-started">Getting Started</a>
      </li>
      <li><a href="#contributing">Contributing</a></li>
      <li><a href="#contact">Contact</a></li>
      <li><a href="#acknowledgments">Acknowledgments</a></li>
   </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

In the first execution, the script asks the user to select a folder to store the xkcds vignettes (in a folder called `xkcd-vignettes`) and explanations (`xkcd-explanations`).
Once that's done, the script will start to download all existing xkcds. On successive runs of the script, it will check if there are any new xkcds available for download.

<!-- INTENDED USAGE -->

### Intended usage

Even though the program works fine as it is, it would be much better if we scheduled it to run on Mondays, Wednesdays and Fridays, the days when new xkcds are released.

There are two ways to do this, depending on the OS that you use:

For **macOS** and **Linux** users:
1. Open a terminal window and run the following command to open a crontab file:
    ```
    crontab -e
    ```
2. Add a new line to the file with the following code:
    ```
    0 19 * * 1,3,5 /usr/bin/python3 /path/to/xkcd-downloader.exe
    ```
   Notice that the hour is set to 19:00, which I think is a reasonable hour to get the xkcd as it will be already released.


3. Save and close the crontab file. The program will now run at the specified time using cron.

For **Windows** users:

1. Open the Task Scheduler by pressing the Windows key and typing "Task Scheduler".
2. Click on the "Create Basic Task" option.
3. Give the task a name and description, then click "Next".
4. Select a trigger for the task. In this case, "Weekly".
5. Choose the days "Monday", "Wednesday" and "Friday".
6. Select the "Start a program" action, then click "Next".
7. In the "Program/script" field, enter the path to the executable, e.g. `C:\Python\Python38\python.exe`.
8. In the "Add arguments" field, enter the path to your script file, e.g. `C:\xkcd-downloader.exe`.
9. Click "Next" and then "Finish".<br>  
   The program should now run at the specified time using the Task Scheduler.

<!-- PROJECT STRUCTURE -->

### Project Structure

Directories:

- `data`: Contains the `xkcd-path.txt`, which stores the path where the xkcds are being stored.
- `src`:  Contains the source code files.

Besides those directories, there are also these two files in the root (apart from the .gitignore, README.md and LICENSE):

- `xkcd-downloader.spec`: Used to generate a .exe file with [PyInstaller](https://pyinstaller.org/en/stable/).
- `requirements.txt`: Lists the names and versions of each package used to build this project.

<!-- BUILT WITH -->

### Built With

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [httpx](https://www.python-httpx.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

If you want to execute the program:
- Go to [releases](https://github.com/HenestrosaConH/xkcd-downloader/releases) and download the latest one. Once you download it open `xkcd-downloader.exe`.

If you want to open the code:
- Clone the project with the `git clone https://github.com/HenestrosaConH/xkcd-downloader.git` command and then open it with your favourite IDE (mine is [PyCharm](https://www.jetbrains.com/pycharm/)).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag `enhancement`.
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

<a href="https://www.linkedin.com/in/henestrosaconh/" target="blank"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="mailto:henestrosaconh@gmail.com" target="_blank"><img alt="Gmail" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

I've made use of the following resources to make this project:

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template/)
- [Img Shields](https://shields.io)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/HenestrosaConH/xkcd-downloader.svg?style=for-the-badge
[contributors-url]: https://github.com/HenestrosaConH/xkcd-downloader/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/HenestrosaConH/xkcd-downloader.svg?style=for-the-badge
[forks-url]: https://github.com/HenestrosaConH/xkcd-downloader/network/members
[stars-shield]: https://img.shields.io/github/stars/HenestrosaConH/xkcd-downloader.svg?style=for-the-badge
[stars-url]: https://github.com/HenestrosaConH/xkcd-downloader/stargazers
[issues-shield]: https://img.shields.io/github/issues/HenestrosaConH/xkcd-downloader.svg?style=for-the-badge
[issues-url]: https://github.com/HenestrosaConH/xkcd-downloader/issues
[linkedin-url]: https://linkedin.com/in/henestrosaconh
