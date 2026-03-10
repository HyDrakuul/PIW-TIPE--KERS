#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 00:21:57 2024

@author: gyanlouisin

TIPE project: GUI testing helper for interruptible functions.

This small script demonstrates how to run a long-running function in a
background thread while keeping a tkinter GUI responsive. It was used to
validate that data acquisition loops can be stopped cleanly.

Skills demonstrated:
 - threading with Python
 - simple tkinter GUI design
 - clean shutdown of background processes
"""

import tkinter as tk
import threading
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Arrêter la fonction")

        self.running = True

        self.label = tk.Label(root, text="Cliquez sur le bouton pour arrêter la fonction")
        self.label.pack(pady=10)

        self.stop_button = tk.Button(root, text="Arrêter", command=self.stop_function)
        self.stop_button.pack(pady=5)

        # Démarrer la fonction dans un thread
        self.thread = threading.Thread(target=self.run_function)
        self.thread.start()

    def run_function(self):
        while self.running:
            print("Fonction en cours d'exécution...")
            # Remplacez cette partie par votre fonction
            time.sleep(1)

    def stop_function(self):
        self.running = False
        print("Fonction arrêtée.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()