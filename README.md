# ✈️ Airline Ticket Price Prediction

A full-stack machine learning application that predicts airline ticket prices from flight details such as airline, route, journey date, departure/arrival time, duration, number of stops, and additional flight information.

The project combines a machine learning pipeline with a FastAPI backend and React frontend to provide an interactive ticket-price prediction system.

---

## Live Project

> Deployment link will be added after production deployment.

**GitHub Repository**

https://github.com/Rishavv75/Airline-Ticket-Prediction

---

## Problem Statement

Airline ticket prices depend on multiple factors including airline, route, number of stops, journey date, departure time, arrival time, duration, and additional flight information.

The objective of this project is to build a machine learning system that learns patterns from historical flight data and estimates the expected ticket price for a new flight.

---

## Project Objectives

- Build an end-to-end airline ticket price prediction system.
- Perform data cleaning and feature engineering.
- Transform categorical and numerical features for machine learning.
- Train and compare multiple regression models.
- Evaluate models using MAE, RMSE, and R².
- Perform cross-validation and error analysis.
- Analyze feature importance.
- Expose the trained model through a FastAPI REST API.
- Build a React-based user interface for predictions.
- Package the final model using Joblib and Git LFS.

---

# Machine Learning Pipeline

The overall workflow is:

```text
Raw Flight Dataset
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ├── Journey Day
        ├── Journey Month
        ├── Journey Weekday
        ├── Departure Hour
        ├── Departure Minute
        ├── Arrival Hour
        ├── Arrival Minute
        └── Duration Minutes
        │
        ▼
Train/Test Split
        │
        ▼
Preprocessing Pipeline
        │
        ├── Numerical Features
        └── Categorical Features
        │
        ▼
Model Training
        │
        ├── Random Forest
        └── XGBoost
        │
        ▼
Model Evaluation
        │
        ├── MAE
        ├── RMSE
        ├── R²
        ├── Cross Validation
        ├── Feature Importance
        └── Error Analysis
        │
        ▼
Final Model
        │
        ▼
FastAPI Prediction API
        │
        ▼
React Frontend