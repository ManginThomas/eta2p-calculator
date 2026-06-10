import tkinter as tk
from tkinter import ttk, messagebox
import threading

stats = None
brentq = None
scipy_loaded = False

def preload_scipy():
    global scipy_loaded, stats, brentq

    from scipy import stats as scipy_stats
    from scipy.optimize import brentq as scipy_brentq

    stats = scipy_stats
    brentq = scipy_brentq

    scipy_loaded = True

    try:
        status_var.set("Prêt")
    except:
        pass

# ==========================================================
# Fonctions statistiques
# ==========================================================

def eta_p2_from_f(F, df1, df2):
    return (F * df1) / (F * df1 + df2)


def eta_to_f(eta):
    if eta >= 1:
        return float("inf")
    return (eta / (1 - eta)) ** 0.5


def lambda_to_eta_p2(lam, df1, df2):
    return lam / (lam + df1 + df2 + 1)


def find_lambda_lower(F_obs, df1, df2, alpha):
    target = 1 - alpha / 2

    def func(lam):
        return stats.ncf.cdf(F_obs, df1, df2, lam) - target

    try:
        return brentq(func, 0, 1e8)
    except ValueError:
        return 0.0


def find_lambda_upper(F_obs, df1, df2, alpha):
    target = alpha / 2

    def func(lam):
        return stats.ncf.cdf(F_obs, df1, df2, lam) - target

    upper = 1.0

    while func(upper) > 0:
        upper *= 2

        if upper > 1e12:
            break

    try:
        return brentq(func, 0, upper)
    except ValueError:
        return float("nan")


def format_p_value(p):
    if p < 0.001:
        return "p < .001"
    else:
        return f"p = {p:.3f}".replace("0.", ".")


# ==========================================================
# Calcul principal
# ==========================================================

def calculate():
    if not scipy_loaded:
        messagebox.showinfo(
         "Chargement",
         "Les bibliothèques statistiques sont encore en cours de chargement."
        )
        return

    try:
        F = float(entry_f.get())
        df1 = float(entry_df1.get())
        df2 = float(entry_df2.get())
        confidence = float(combo_ci.get())

        alpha = 1 - confidence / 100

        # p-value
        p = stats.f.sf(F, df1, df2)

        # η²p
        eta = eta_p2_from_f(F, df1, df2)

        # Cohen's f
        cohen_f = eta_to_f(eta)

        # IC
        if ci_type.get() == "one-sided":

            lambda_l = find_lambda_lower(F, df1, df2, alpha)

            eta_l = lambda_to_eta_p2(lambda_l, df1, df2)
            eta_u = 1.0

        else:

            lambda_l = find_lambda_lower(F, df1, df2, alpha)
            lambda_u = find_lambda_upper(F, df1, df2, alpha)

            eta_l = lambda_to_eta_p2(lambda_l, df1, df2)
            eta_u = lambda_to_eta_p2(lambda_u, df1, df2)
        
        # IC de Cohen's f
        f_l = eta_to_f(eta_l)
        f_u = eta_to_f(eta_u)

        if f_u == float("inf"):
            f_ci_text = f"[{f_l:.3f} ; ∞]"
        else:
            f_ci_text = f"[{f_l:.3f} ; {f_u:.3f}]"

        result_text = (
            f"η²p = {eta:.3f}\n"
            f"IC{int(confidence)}% (η²p) = [{eta_l:.3f} ; {eta_u:.3f}]\n\n"
            f"Cohen's f = {cohen_f:.3f}\n"
            f"IC{int(confidence)}% (f) = {f_ci_text}\n\n"
            f"{format_p_value(p)}"
        )

        result_var.set(result_text)

    except Exception as e:
        messagebox.showerror("Erreur", str(e))


# ==========================================================
# Copier les résultats
# ==========================================================

def copy_results():

    text = result_var.get()

    if not text.strip():
        return

    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

    messagebox.showinfo(
        "Copié",
        "Les résultats ont été copiés dans le presse-papiers."
    )

# ==========================================================
# Interface graphique
# ==========================================================

root = tk.Tk()
root.title("Calculateur η²p")
root.geometry("400x550")
root.resizable(True, True)

main = ttk.Frame(root, padding=15)
main.pack(fill="both", expand=True)

# ---------- Entrées ----------

ttk.Label(main, text="Valeur de F").grid(
    row=0, column=0, sticky="w", pady=5
)

entry_f = ttk.Entry(main, width=15)
entry_f.grid(row=0, column=1, sticky="w")

ttk.Label(main, text="df effet").grid(
    row=1, column=0, sticky="w", pady=5
)

entry_df1 = ttk.Entry(main, width=15)
entry_df1.grid(row=1, column=1, sticky="w")

ttk.Label(main, text="df erreur").grid(
    row=2, column=0, sticky="w", pady=5
)

entry_df2 = ttk.Entry(main, width=15)
entry_df2.grid(row=2, column=1, sticky="w")

ttk.Label(main, text="Niveau d'IC (%)").grid(
    row=3, column=0, sticky="w", pady=5
)

combo_ci = ttk.Combobox(
    main,
    values=["90", "95", "99"],
    width=12,
    state="readonly"
)

combo_ci.current(1)
combo_ci.grid(row=3, column=1, sticky="w")

# ---------- Type d'IC ----------

ttk.Label(main, text="Type d'IC").grid(
    row=4, column=0, sticky="w", pady=10
)

ci_type = tk.StringVar(value="two-sided")

ttk.Radiobutton(
    main,
    text="Bilatéral",
    variable=ci_type,
    value="two-sided"
).grid(row=4, column=1, sticky="w")

ttk.Radiobutton(
    main,
    text="Unilatéral (effectsize)",
    variable=ci_type,
    value="one-sided"
).grid(row=5, column=1, sticky="w")

# ---------- Bouton calcul ----------

ttk.Button(
    main,
    text="Calculer",
    command=calculate
).grid(
    row=7,
    column=0,
    columnspan=2,
    pady=20
)

# ---------- Résultats ----------

result_var = tk.StringVar()

status_var = tk.StringVar(value="Chargement des bibliothèques...")

result_label = ttk.Label(
    main,
    textvariable=result_var,
    justify="left",
    font=("Segoe UI", 11)
)
status_label = ttk.Label(
    main,
    textvariable=status_var
)

status_label.grid(
    row=6,
    column=0,
    columnspan=2,
    sticky="w",
    pady=5
)

result_label.grid(
    row=8,
    column=0,
    columnspan=2,
    sticky="w",
    pady=10
)

# ---------- Copier ----------

ttk.Button(
    main,
    text="Copier les résultats",
    command=copy_results
).grid(
    row=9,
    column=0,
    columnspan=2,
    pady=15
)

# ---------- Lancement ----------
threading.Thread(
    target=preload_scipy,
    daemon=True
).start()

root.mainloop()