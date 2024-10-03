# Spotify Project

## Overview

This project is an integration of the **Spotify API** to fetch the user's liked songs and allow the download of music videos from YouTube. The backend and frontend are separated into two distinct projects: one for handling the backend using Flask and another for the frontend built with React.

Before running the application, you will need to obtain credentials from Spotify to authenticate users and interact with the Spotify API. Please follow the instructions below to set up your Spotify Developer account and generate the necessary API credentials.

---

## Obtain Spotify API Credentials

In order to interact with the Spotify Web API, you need to register your application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

### Steps to Obtain Your Credentials:

1. **Create a Spotify Developer Account**:
   - Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Log in with your Spotify account or create a new one.

2. **Create a New Spotify Application**:
   - Once logged in, click on **"Create an App"**.
   - Fill in the application name and description.
   - Agree to the terms and conditions, and click **"Create"**.

3. **Obtain Your API Credentials**:
   - After creating your application, you will be able to see your **Client ID** and **Client Secret**.
   - Keep these credentials private, as they allow access to the Spotify API.

4. **Set Redirect URI**:
   - You need to set a redirect URI for your application to handle authentication.
   - In the Spotify Developer Dashboard, under your app settings, find the **Redirect URIs** section and add `http://localhost:5000/callback` (or whatever your backend URL is).
   - This will be the URL where Spotify will redirect after successful login.

5. **Update Your Application with the Credentials**:
   - In your backend project (`spotifyback`), find the file where credentials are stored (usually in a config file or environment variables).
   - Add your **Client ID**, **Client Secret**, and the **Redirect URI** you just set.

---

## Technologies Used

- **Backend**:
  - **Flask**: Python web framework for building the backend API.
  - **Spotipy**: Python library for interacting with the Spotify Web API.
  - **requests**: For making HTTP requests to external APIs like YouTube.
  
- **Frontend**:
  - **React**: JavaScript library for building the user interface.
  - **React-Scripts**: For running and building the React application.
  - **concurrently**: To run both backend and frontend simultaneously with a single command (if desired).
  
- **Others**:
  - **npm**: For managing frontend dependencies.
  - **Python**: For running the backend and managing dependencies.
  - **Git**: For version control.
  - **YouTube API**: To search and download YouTube videos.

---

## Setup and Installation

### Prerequisites

1. **Node.js** (for React frontend)
2. **Python 3** (for Flask backend)
3. **Spotify Developer Account** (for API access)
4. **YouTube API Key** (for video download functionality)

### Step 1: Clone the repository

Clone the project repository to your local machine:
```bash
git clone https://github.com/yourusername/SpotfyProject.git
cd SpotfyProject
```
Step 2: Install backend dependencies
Navigate to the backend directory and install the required Python packages:

```bash
cd spotifyback
pip install -r requirements.txt
```
Step 3: Install frontend dependencies
Navigate to the frontend directory and install the required npm packages:

```bash
cd spotifyfront
npm install
```
Running the Application
Running Backend
To run the backend (Flask) separately, navigate to the spotifyback folder and use the following command:

```bash
cd spotifyback
flask run
```
The backend will now be running.

Running Frontend
To run the frontend (React) separately, navigate to the spotifyfront folder and use the following command:

```bash
Copiar código
cd spotifyfront
npm start
```
The application will now be running on http://localhost:3000/.

How to Use
Login with Spotify: Upon running the application, you will be redirected to a Spotify login screen. After logging in, you will be sent back to the app.
Select Your Liked Songs: Once logged in, you will be shown a list of your liked songs on Spotify. Select the songs you wish to download.
Download Music Video: After selecting the songs, the application will automatically fetch and download the corresponding music videos from YouTube to your local machine.
Troubleshooting
If you encounter errors during setup or execution, consider the following solutions:

Proxy Errors: Ensure that the backend is running before starting the frontend. If you get a proxy error, make sure the Flask server is running on port 5000.
Missing Dependencies: Make sure all required dependencies are installed by running npm install for the frontend and pip install -r requirements.txt for the backend.
API Errors: Verify that your Spotify Developer credentials and YouTube API key are correctly configured in the backend.
License
This project is open-source.

Authors
Davi Ruas
