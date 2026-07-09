# 🚀 DevFolio - Professional AI Engineer Portfolio & CMS

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A high-performance, dynamic portfolio and Content Management System (CMS) built to showcase engineering projects, technical blogs, and research in Agentic AI, LLM systems, and Deep Learning. 

🔗 **Live Demo:** [https://devfolio-kd0g.onrender.com](https://devfolio-kd0g.onrender.com)

---

## 📸 Project Screenshots

*(Upload your screenshots in your GitHub repo and replace the links below)*

| Home Page | Projects Section |
| :---: | :---: |
| <img src="https://via.placeholder.com/600x350/131626/5b5ef4?text=Upload+Home+Screenshot" alt="Home" width="100%"> | <img src="https://via.placeholder.com/600x350/131626/5b5ef4?text=Upload+Projects+Screenshot" alt="Projects" width="100%"> |

| Blog CMS | Mobile Responsive View |
| :---: | :---: |
| <img src="https://via.placeholder.com/600x350/131626/5b5ef4?text=Upload+Blog+Screenshot" alt="Blog" width="100%"> | <img src="https://via.placeholder.com/300x500/131626/5b5ef4?text=Upload+Mobile+Screenshot" alt="Mobile" width="60%"> |

---

## 🏗️ Architecture & Tech Stack

This project is built with a decoupled database architecture, ensuring maximum scalability and data safety during cloud deployments.

### Backend: Django (Python)
- **Framework:** Leverages Django's robust MTV (Model-Template-View) architecture for secure and rapid development.
- **Admin CMS:** Fully customized Django Admin interface to seamlessly manage blog posts, project listings, and resume updates without touching the codebase.
- **Security:** Implements environment variables (`.env`) for secret keys and database credentials, strictly ignoring them from version control.

### Database: Neon (Serverless PostgreSQL)
- **Why Neon?** Replaced the default local SQLite with Neon’s serverless PostgreSQL. This ensures that the database compute and storage are decoupled from the hosting server. If the Render web server goes to sleep or restarts, the data remains persistently secure and instantly accessible.
- **Connection:** Managed securely via `dj-database-url` and parsed dynamically through Python's `urllib`.

### Deployment & Infrastructure: Render
- **Web Server:** Uses **Gunicorn** (Green Unicorn) as a Python WSGI HTTP Server for UNIX, providing a robust production environment.
- **Static File Management:** Integrated **WhiteNoise** middleware to serve static files (CSS, JS, Images) directly from the Django application, eliminating the need for a separate Nginx/Apache configuration for static assets on the PaaS.
- **CI/CD:** Automated deployment pipeline linked directly to the `main` GitHub branch.

### Frontend 
- **UI/UX:** Classic Tech Professional aesthetic prioritizing readability and content hierarchy.
- **Styling:** Custom CSS with strict adherence to a 4px/8px spacing grid and optimized typography (Inter & JetBrains Mono).
- **Responsive:** Fluid layouts that scale perfectly from 4K desktop monitors down to mobile devices.

---

## ✨ Key Features

- **Dynamic Data Rendering:** All projects, skills, and blogs are fetched in real-time from the PostgreSQL database.
- **Markdown/Rich Text Support:** Write and publish technical blogs directly from the admin panel.
- **Seamless Static-to-Dynamic Routing:** Integrates static resume downloads and contact endpoints elegantly with the dynamic backend.
- **Production-Ready Security:** Debug mode disabled, allowed hosts strictly configured, and environment variables actively utilized.

---

## 🛠️ Local Development Setup

Want to run this project locally? Follow these steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/bappyBDN/your-repo-name.git](https://github.com/bappyBDN/your-repo-name.git)
cd your-repo-name
