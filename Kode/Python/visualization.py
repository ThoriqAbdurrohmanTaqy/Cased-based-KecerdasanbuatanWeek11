import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import openpyxl
from fuzzy import get_kelayakan_score, fuzzify_pelayanan, fuzzify_harga

# Set style
plt.style.use('seaborn-v0_8-muted')

def plot_membership_functions():
    # 1. Pelayanan
    x_p = np.linspace(0, 100, 500)
    y_buruk = [fuzzify_pelayanan(i)['buruk'] for i in x_p]
    y_biasa = [fuzzify_pelayanan(i)['biasa'] for i in x_p]
    y_bagus = [fuzzify_pelayanan(i)['bagus'] for i in x_p]

    plt.figure(figsize=(10, 4))
    plt.plot(x_p, y_buruk, label='Buruk', color='red', linewidth=2)
    plt.plot(x_p, y_biasa, label='Biasa', color='orange', linewidth=2)
    plt.plot(x_p, y_bagus, label='Bagus', color='green', linewidth=2)
    plt.title('Fungsi Keanggotaan: Kualitas Pelayanan')
    plt.xlabel('Nilai Pelayanan (1-100)')
    plt.ylabel('Derajat Keanggotaan (\u03bc)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('mf_pelayanan.png')
    plt.close()

    # 2. Harga
    x_h = np.linspace(25000, 55000, 500)
    y_murah = [fuzzify_harga(i)['murah'] for i in x_h]
    y_sedang = [fuzzify_harga(i)['sedang'] for i in x_h]
    y_mahal = [fuzzify_harga(i)['mahal'] for i in x_h]

    plt.figure(figsize=(10, 4))
    plt.plot(x_h, y_murah, label='Murah', color='blue', linewidth=2)
    plt.plot(x_h, y_sedang, label='Sedang', color='purple', linewidth=2)
    plt.plot(x_h, y_mahal, label='Mahal', color='brown', linewidth=2)
    plt.title('Fungsi Keanggotaan: Harga')
    plt.xlabel('Harga (Rupiah)')
    plt.ylabel('Derajat Keanggotaan (\u03bc)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('mf_harga.png')
    plt.close()

def plot_results():
    # Load data
    df = pd.read_excel('restoran.xlsx')
    df['score'] = df.apply(lambda row: get_kelayakan_score(row['Pelayanan'], row['harga']), axis=1)

    # 3. Scatter Plot: Pelayanan vs Harga
    plt.figure(figsize=(10, 6))
    sc = plt.scatter(df['Pelayanan'], df['harga'], c=df['score'], cmap='viridis', s=100, edgecolors='white', alpha=0.8)
    plt.colorbar(sc, label='Skor Kelayakan (Fuzzy)')
    plt.title('Distribusi Restoran: Pelayanan vs Harga')
    plt.xlabel('Kualitas Pelayanan')
    plt.ylabel('Harga')
    
    # Highlight top 5
    top_5 = df.nlargest(5, 'score')
    plt.scatter(top_5['Pelayanan'], top_5['harga'], color='red', s=150, marker='*', label='Top 5')
    for i, txt in enumerate(top_5['id Pelanggan']):
        plt.annotate(f"ID:{txt}", (top_5.iloc[i]['Pelayanan'], top_5.iloc[i]['harga']), xytext=(5,5), textcoords='offset points')
    
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('hasil_visualisasi.png')
    plt.close()

    # 4. Bar Chart Top 5
    plt.figure(figsize=(8, 5))
    top_5 = top_5.sort_values('score', ascending=True)
    plt.barh(top_5['id Pelanggan'].astype(str), top_5['score'], color='teal')
    plt.title('Top 5 Restoran Terbaik (Skor Fuzzy)')
    plt.xlabel('Skor Kelayakan')
    plt.ylabel('ID Restoran')
    plt.xlim(0, 110)
    for i, v in enumerate(top_5['score']):
        plt.text(v + 1, i, str(round(v, 2)), color='black', va='center')
    plt.savefig('top5_bar.png')
    plt.close()

if __name__ == "__main__":
    print("Memproses visualisasi...")
    plot_membership_functions()
    plot_results()
    print("Selesai! Gambar visualisasi telah disimpan sebagai file .png")
