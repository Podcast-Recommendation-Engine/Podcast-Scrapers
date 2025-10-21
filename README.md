# Podcast-Scrapers

## Overview

This repository is dedicated to developing and managing a set of **web scrapers** that extract podcast data directly from various **websites and online sources**.  
The goal is to **collect, clean, and standardize** podcast metadata and episode information to feed into the **Podcast Recommendation Platform**.

The scrapers should be modular, reliable, and easily extendable to support new podcast directories or sites.

---

## Documentation Requirements

The documentation should clearly explain:

* List of websites and sources being scraped  
* Scraper architecture and crawling flow  
* Data fields extracted (title, author, category, URL, episode details, etc.)  
* Steps to run scrapers manually or automatically (cron jobs, Celery, etc.)  
* Storage strategy (MongoDB, JSON files, Elasticsearch, etc.)  
* Error handling, rate limiting, and anti-blocking techniques (headers, delays, proxies)  

---

## Features

- Web scraping from multiple podcast platforms and websites  
- Extraction of podcast metadata (name, description, category, rating, etc.)  
- Extraction of episode information (title, duration, publish date, etc.)  
- Data cleaning and normalization for downstream processing  
- Logging, retry, and monitoring mechanisms  
- Modular structure to easily add new website scrapers  

---
