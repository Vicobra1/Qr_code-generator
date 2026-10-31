"""Kobra QR — a friendly, local QR-code generator built with Tkinter."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urlsplit

import qrcode
from PIL import Image, ImageTk


BACKGROUND = "#10151e"
SIDEBAR = "#0b1017"
SURFACE = "#171e29"
SURFACE_LIGHT = "#1c2532"
TEXT = "#f2f5f8"
MUTED = "#9aa8b8"
SUBTLE = "#68788b"
LINE = "#293444"
ACCENT = "#55d6c2"
ACCENT_DARK = "#163c3a"
ERROR = "#f28d8d"

INK_COLORS = {
    "Noir": "#111827",
    "Bleu nuit": "#17243a",
    "Vert pétrole": "#0f766e",
}
PAPER_COLORS = {
    "Blanc": "#ffffff",
    "Ivoire": "#fffdf5",
    "Menthe claire": "#e8faf5",
}
QR_SIZES = {"Petit": 8, "Moyen": 12, "Grand": 18}


class KobraQR:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Kobra QR — Créateur de QR codes")
        self.root.geometry("1040x720")
        self.root.minsize(820, 620)
        self.root.configure(bg=BACKGROUND)
        self.root.option_add("*Font", ("Segoe UI", 10))

        self.current_image: Image.Image | None = None
        self.preview_photo: ImageTk.PhotoImage | None = None
        self.fields: dict[str, tk.Widget | tk.Variable] = {}
        self.kind_var = tk.StringVar(value="Lien web")
        self.ink_var = tk.StringVar(value="Noir")
        self.paper_var = tk.StringVar(value="Blanc")
        self.size_var = tk.StringVar(value="Moyen")
        self.status_var = tk.StringVar(value="Prêt à créer votre QR code.")

        self._configure_styles()
        self._build_layout()
        self._build_content_fields()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Kobra.TCombobox", fieldbackground=SURFACE_LIGHT,
            background=SURFACE_LIGHT, foreground=TEXT, arrowcolor=ACCENT,
            bordercolor=LINE, lightcolor=LINE, darkcolor=LINE, padding=8,
        )
        style.map(
            "Kobra.TCombobox",
            fieldbackground=[("readonly", SURFACE_LIGHT)],
            foreground=[("readonly", TEXT)],
            selectbackground=[("readonly", SURFACE_LIGHT)],
            selectforeground=[("readonly", TEXT)],
        )

    @staticmethod
    def _label(parent: tk.Widget, text: str, *, color: str = MUTED,
               size: int = 10, weight: str = "normal") -> tk.Label:
        return tk.Label(parent, text=text, bg=parent.cget("bg"), fg=color,
                        font=("Segoe UI", size, weight), anchor="w")

    def _build_layout(self) -> None:
        header = tk.Frame(self.root, bg=SIDEBAR, height=78)
        header.pack(fill="x")
        header.pack_propagate(False)

        brand = tk.Frame(header, bg=SIDEBAR)
        brand.pack(side="left", padx=28, pady=15)
        tk.Label(brand, text="K", bg=ACCENT, fg="#10201f", width=2,
                 font=("Segoe UI", 18, "bold"), padx=5, pady=2).pack(side="left", padx=(0, 12))
        brand_text = tk.Frame(brand, bg=SIDEBAR)
        brand_text.pack(side="left")
        tk.Label(brand_text, text="KOBRA QR", bg=SIDEBAR, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(brand_text, text="CRÉATEUR DE QR CODES", bg=SIDEBAR,
                 fg=SUBTLE, font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(1, 0))
        tk.Label(header, text="Version 2 · Projet d’apprentissage", bg=SIDEBAR,
                 fg=SUBTLE, font=("Segoe UI", 9)).pack(side="right", padx=28)

        body = tk.Frame(self.root, bg=BACKGROUND)
        body.pack(fill="both", expand=True, padx=28, pady=(22, 16))
        body.grid_columnconfigure(0, weight=11, uniform="content")
        body.grid_columnconfigure(1, weight=9, uniform="content")
        body.grid_rowconfigure(0, weight=1)

        self.form_card = tk.Frame(body, bg=SURFACE, highlightthickness=1, highlightbackground=LINE)
        self.form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.preview_card = tk.Frame(body, bg=SURFACE, highlightthickness=1, highlightbackground=LINE)
        self.preview_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self._build_form_card()
        self._build_preview_card()

        footer = tk.Frame(self.root, bg=BACKGROUND)
        footer.pack(fill="x", padx=29, pady=(0, 14))
        self._label(footer, "Kobra QR  ·  Un projet personnel en évolution", size=9, color=SUBTLE).pack(side="left")
        self._label(footer, "Tout est généré localement sur cet ordinateur", size=9, color=SUBTLE).pack(side="right")

    def _build_form_card(self) -> None:
        card = self.form_card
        self._label(card, "VOTRE QR CODE", size=9, weight="bold", color=ACCENT).pack(anchor="w", padx=22, pady=(22, 5))
        self._label(card, "Que souhaitez-vous partager ?", size=19, weight="bold", color=TEXT).pack(anchor="w", padx=22)
        self._label(card, "Choisissez un format puis saisissez son contenu.", size=10).pack(anchor="w", padx=22, pady=(4, 18))

        self._label(card, "TYPE DE CONTENU", size=9, weight="bold").pack(anchor="w", padx=22, pady=(0, 6))
        kind = ttk.Combobox(card, textvariable=self.kind_var,
                            values=("Lien web", "Texte libre", "Carte de contact", "Réseau Wi-Fi"),
                            state="readonly", style="Kobra.TCombobox")
        kind.pack(fill="x", padx=22)
        kind.bind("<<ComboboxSelected>>", lambda _event: self._build_content_fields())
        self.content_frame = tk.Frame(card, bg=SURFACE)
        self.content_frame.pack(fill="both", expand=True, padx=22, pady=(14, 10))

        options = tk.Frame(card, bg=SURFACE)
        options.pack(fill="x", padx=22, pady=(0, 14))
        self._label(options, "APPARENCE", size=9, weight="bold").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 7))
        options.grid_columnconfigure(0, weight=1)
        options.grid_columnconfigure(1, weight=1)
        self._label(options, "Couleur du code").grid(row=1, column=0, sticky="w", pady=(0, 4))
        self._label(options, "Fond").grid(row=1, column=1, sticky="w", pady=(0, 4))
        ttk.Combobox(options, textvariable=self.ink_var, values=tuple(INK_COLORS), state="readonly", style="Kobra.TCombobox").grid(row=2, column=0, sticky="ew", padx=(0, 6))
        ttk.Combobox(options, textvariable=self.paper_var, values=tuple(PAPER_COLORS), state="readonly", style="Kobra.TCombobox").grid(row=2, column=1, sticky="ew", padx=(6, 0))
        self._label(options, "Taille du fichier").grid(row=3, column=0, sticky="w", pady=(10, 4))
        ttk.Combobox(options, textvariable=self.size_var, values=tuple(QR_SIZES), state="readonly", style="Kobra.TCombobox", width=10).grid(row=4, column=0, sticky="w")

        actions = tk.Frame(card, bg=SURFACE)
        actions.pack(fill="x", padx=22, pady=(0, 20))
        self._button(actions, "Créer l’aperçu", self.generate, primary=True).pack(side="left", fill="x", expand=True)
        self.save_button = self._button(actions, "Enregistrer PNG", self.save_image, primary=False)
        self.save_button.pack(side="left", padx=(9, 0))
        self.save_button.configure(state="disabled")

    def _build_preview_card(self) -> None:
        card = self.preview_card
        self._label(card, "APERÇU", size=9, weight="bold", color=ACCENT).pack(anchor="w", padx=22, pady=(22, 5))
        self._label(card, "Votre création", size=19, weight="bold", color=TEXT).pack(anchor="w", padx=22)
        self._label(card, "Le rendu apparaîtra ici avant l’enregistrement.", size=10).pack(anchor="w", padx=22, pady=(4, 15))
        self.preview_area = tk.Frame(card, bg="#202a37", highlightthickness=1, highlightbackground=LINE)
        self.preview_area.pack(fill="both", expand=True, padx=22, pady=(0, 15))
        self.preview_area.grid_rowconfigure(0, weight=1)
        self.preview_area.grid_columnconfigure(0, weight=1)
        self.preview_label = tk.Label(self.preview_area, text="▦\n\nVotre QR code\nsera affiché ici",
                                      bg="#202a37", fg=SUBTLE, font=("Segoe UI", 13), justify="center")
        self.preview_label.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self._label(card, "CONSEIL", size=9, weight="bold", color=ACCENT).pack(anchor="w", padx=22)
        self._label(card, "Testez le code avec l’appareil photo de votre téléphone avant de le partager.", size=9).pack(anchor="w", padx=22, pady=(4, 14))
        self.status_label = tk.Label(card, textvariable=self.status_var, bg=SURFACE, fg=MUTED, font=("Segoe UI", 9), anchor="w")
        self.status_label.pack(fill="x", padx=22, pady=(0, 19))

    def _build_content_fields(self) -> None:
        for child in self.content_frame.winfo_children():
            child.destroy()
        self.fields.clear()
        kind = self.kind_var.get()

        if kind in ("Lien web", "Texte libre"):
            label = "ADRESSE DU LIEN" if kind == "Lien web" else "VOTRE TEXTE"
            hint = "Ex. : https://exemple.com" if kind == "Lien web" else "Saisissez le texte que vous souhaitez partager."
            self._label(self.content_frame, label, size=9, weight="bold").pack(anchor="w", pady=(0, 6))
            self._label(self.content_frame, hint, size=9, color=SUBTLE).pack(anchor="w", pady=(0, 5))
            text = tk.Text(self.content_frame, height=5, wrap="word", undo=True,
                           bg=SURFACE_LIGHT, fg=TEXT, insertbackground=ACCENT,
                           selectbackground=ACCENT_DARK, relief="flat", bd=0,
                           highlightthickness=1, highlightbackground=LINE,
                           highlightcolor=ACCENT, padx=10, pady=9,
                           font=("Segoe UI", 10))
            text.pack(fill="x", expand=True)
            self.fields["content"] = text
            return

        if kind == "Carte de contact":
            self.content_frame.grid_columnconfigure(0, weight=1, uniform="contact")
            self.content_frame.grid_columnconfigure(1, weight=1, uniform="contact")
            self._add_entry("Nom complet *", "name", row=0, column=0)
            self._add_entry("Téléphone", "phone", row=0, column=1)
            self._add_entry("Adresse e-mail", "email", row=1, column=0)
            self._add_entry("Organisation", "organization", row=1, column=1)
            self._label(self.content_frame, "Le nom complet est obligatoire.", size=9, color=SUBTLE).grid(row=4, column=0, columnspan=2, sticky="w", pady=(3, 0))
            return

        self._add_entry("Nom du réseau (SSID) *", "ssid")
        self._add_entry("Mot de passe", "wifi_password")
        self._label(self.content_frame, "Sécurité", size=9, weight="bold").pack(anchor="w", pady=(0, 5))
        security = ttk.Combobox(self.content_frame, values=("WPA/WPA2", "WEP", "Aucun"), state="readonly", style="Kobra.TCombobox")
        security.set("WPA/WPA2")
        security.pack(fill="x")
        self.fields["security"] = security
        hidden_var = tk.BooleanVar(value=False)
        hidden = tk.Checkbutton(self.content_frame, text="Réseau masqué", variable=hidden_var,
                                bg=SURFACE, fg=MUTED, activebackground=SURFACE,
                                activeforeground=TEXT, selectcolor=SURFACE_LIGHT,
                                font=("Segoe UI", 9))
        hidden.pack(anchor="w", pady=(8, 0))
        self.fields["hidden"] = hidden_var

    def _add_entry(self, label: str, key: str, *, row: int | None = None,
                   column: int = 0) -> None:
        label_widget = self._label(self.content_frame, label, size=9, weight="bold")
        entry = tk.Entry(self.content_frame, bg=SURFACE_LIGHT, fg=TEXT,
                         insertbackground=ACCENT, relief="flat", bd=0,
                         highlightthickness=1, highlightbackground=LINE,
                         highlightcolor=ACCENT, font=("Segoe UI", 10))
        if row is None:
            label_widget.pack(anchor="w", pady=(0, 5))
            entry.pack(fill="x", ipady=8, pady=(0, 10))
        else:
            label_widget.grid(row=row * 2, column=column, sticky="w", padx=(0, 9), pady=(0, 4))
            entry.grid(row=row * 2 + 1, column=column, sticky="ew", padx=(0, 9), ipady=7, pady=(0, 8))
        self.fields[key] = entry

    @staticmethod
    def _button(parent: tk.Widget, text: str, command, *, primary: bool) -> tk.Button:
        if primary:
            background, foreground, active = ACCENT, "#10201f", "#35b8a7"
        else:
            background, foreground, active = SURFACE_LIGHT, TEXT, "#2a3747"
        return tk.Button(parent, text=text, command=command, bg=background, fg=foreground,
                         activebackground=active, activeforeground=foreground,
                         relief="flat", bd=0, padx=14, pady=10,
                         font=("Segoe UI", 9, "bold"), cursor="hand2",
                         disabledforeground=SUBTLE)

    @staticmethod
    def _escape_vcard(value: str) -> str:
        return value.replace("\\", "\\\\").replace(";", r"\;").replace(",", r"\,").replace("\n", r"\n")

    @staticmethod
    def _escape_wifi(value: str) -> str:
        special_characters = "\\;,:\""
        return "".join("\\" + char if char in special_characters else char for char in value)

    def _get_payload(self) -> str:
        kind = self.kind_var.get()
        if kind in ("Lien web", "Texte libre"):
            payload = self.fields["content"].get("1.0", "end-1c").strip()
            if not payload:
                raise ValueError("Saisissez une adresse ou un texte avant de créer le QR code.")
            if kind == "Lien web" and not payload.lower().startswith(("https://", "http://")):
                payload = "https://" + payload
            if kind == "Lien web":
                parsed_url = urlsplit(payload)
                if parsed_url.scheme not in ("http", "https") or not parsed_url.hostname:
                    raise ValueError("Saisissez un lien web valide, par exemple https://exemple.com.")
            return payload

        if kind == "Carte de contact":
            name = self.fields["name"].get().strip()
            if not name:
                raise ValueError("Saisissez au moins le nom du contact.")
            lines = ["BEGIN:VCARD", "VERSION:3.0", f"FN:{self._escape_vcard(name)}"]
            for key, prefix in (("phone", "TEL"), ("email", "EMAIL"), ("organization", "ORG")):
                value = self.fields[key].get().strip()
                if value:
                    lines.append(f"{prefix}:{self._escape_vcard(value)}")
            lines.append("END:VCARD")
            return "\r\n".join(lines)

        ssid = self.fields["ssid"].get().strip()
        if not ssid:
            raise ValueError("Saisissez le nom du réseau Wi-Fi.")
        security = self.fields["security"].get()
        password = self.fields["wifi_password"].get()
        if security != "Aucun" and not password:
            raise ValueError("Saisissez le mot de passe du réseau ou choisissez « Aucun ».")
        security_code = {"WPA/WPA2": "WPA", "WEP": "WEP", "Aucun": "nopass"}[security]
        hidden = "true" if self.fields["hidden"].get() else "false"
        return f"WIFI:T:{security_code};S:{self._escape_wifi(ssid)};P:{self._escape_wifi(password)};H:{hidden};;"

    def generate(self) -> None:
        try:
            payload = self._get_payload()
            qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M,
                               box_size=QR_SIZES[self.size_var.get()], border=4)
            qr.add_data(payload)
            qr.make(fit=True)
            image = qr.make_image(fill_color=INK_COLORS[self.ink_var.get()],
                                  back_color=PAPER_COLORS[self.paper_var.get()]).get_image().convert("RGB")
            self.current_image = image
            self._show_preview(image)
            self.save_button.configure(state="normal")
            self.status_var.set("Aperçu prêt. Scannez-le avant de le partager.")
            self.status_label.configure(fg=ACCENT)
        except (ValueError, KeyError) as error:
            messagebox.showinfo("Quelques informations sont nécessaires", str(error), parent=self.root)
        except Exception as error:
            messagebox.showerror("Création impossible", f"Le QR code n’a pas pu être généré.\n\nDétail : {error}", parent=self.root)
            self.status_var.set("La création a échoué. Vérifiez les informations et réessayez.")
            self.status_label.configure(fg=ERROR)

    def _show_preview(self, image: Image.Image) -> None:
        preview = image.copy()
        resampling = getattr(Image, "Resampling", Image).NEAREST
        preview.thumbnail((360, 360), resampling)
        self.preview_photo = ImageTk.PhotoImage(preview)
        self.preview_label.configure(image=self.preview_photo, text="", bg=PAPER_COLORS[self.paper_var.get()])

    def save_image(self) -> None:
        if self.current_image is None:
            return
        file_path = filedialog.asksaveasfilename(
            parent=self.root, title="Enregistrer le QR code",
            defaultextension=".png", initialfile="mon_qrcode.png",
            filetypes=[("Image PNG", "*.png")],
        )
        if not file_path:
            return
        try:
            self.current_image.save(Path(file_path), format="PNG")
        except OSError as error:
            messagebox.showerror("Enregistrement impossible", f"Le fichier n’a pas pu être enregistré.\n\n{error}", parent=self.root)
            return
        self.status_var.set(f"QR code enregistré : {Path(file_path).name}")
        self.status_label.configure(fg=ACCENT)
        messagebox.showinfo("C’est enregistré", f"Votre QR code a été enregistré ici :\n{file_path}", parent=self.root)


def main() -> None:
    root = tk.Tk()
    KobraQR(root)
    root.mainloop()


if __name__ == "__main__":
    main()
