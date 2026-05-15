import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from fuzzy import get_kelayakan_score, fuzzify_pelayanan, fuzzify_harga

# Configuration for Premium Aesthetics
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Roboto', 'Arial']
plt.rcParams['axes.facecolor'] = '#121212'
plt.rcParams['figure.facecolor'] = '#121212'
plt.rcParams['text.color'] = '#E0E0E0'
plt.rcParams['axes.labelcolor'] = '#E0E0E0'
plt.rcParams['xtick.color'] = '#B0B0B0'
plt.rcParams['ytick.color'] = '#B0B0B0'
plt.rcParams['grid.color'] = '#333333'
plt.rcParams['axes.edgecolor'] = '#444444'

def plot_membership_premium():
    # 1. Pelayanan
    x_p = np.linspace(0, 100, 500)
    y_buruk = [fuzzify_pelayanan(i)['buruk'] for i in x_p]
    y_biasa = [fuzzify_pelayanan(i)['biasa'] for i in x_p]
    y_bagus = [fuzzify_pelayanan(i)['bagus'] for i in x_p]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(x_p, y_buruk, color='#FF5252', alpha=0.3, label='Buruk')
    ax.plot(x_p, y_buruk, color='#FF5252', linewidth=3)
    
    ax.fill_between(x_p, y_biasa, color='#FFAB40', alpha=0.3, label='Biasa')
    ax.plot(x_p, y_biasa, color='#FFAB40', linewidth=3)
    
    ax.fill_between(x_p, y_bagus, color='#69F0AE', alpha=0.3, label='Bagus')
    ax.plot(x_p, y_bagus, color='#69F0AE', linewidth=3)

    ax.set_title('Membership Functions: Service Quality', fontsize=16, pad=20, fontweight='bold', color='white')
    ax.set_xlabel('Service Score', fontsize=12)
    ax.set_ylabel('Degree of Membership (\u03bc)', fontsize=12)
    ax.legend(frameon=False, fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('premium_mf_pelayanan.png', dpi=300)
    plt.close()

    # 2. Harga
    x_h = np.linspace(25000, 55000, 500)
    y_murah = [fuzzify_harga(i)['murah'] for i in x_h]
    y_sedang = [fuzzify_harga(i)['sedang'] for i in x_h]
    y_mahal = [fuzzify_harga(i)['mahal'] for i in x_h]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(x_h, y_murah, color='#40C4FF', alpha=0.3, label='Murah')
    ax.plot(x_h, y_murah, color='#40C4FF', linewidth=3)
    
    ax.fill_between(x_h, y_sedang, color='#E040FB', alpha=0.3, label='Sedang')
    ax.plot(x_h, y_sedang, color='#E040FB', linewidth=3)
    
    ax.fill_between(x_h, y_mahal, color='#FF8A65', alpha=0.3, label='Mahal')
    ax.plot(x_h, y_mahal, color='#FF8A65', linewidth=3)

    ax.set_title('Membership Functions: Price', fontsize=16, pad=20, fontweight='bold', color='white')
    ax.set_xlabel('Price (Rupiah)', fontsize=12)
    ax.set_ylabel('Degree of Membership (\u03bc)', fontsize=12)
    ax.legend(frameon=False, fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('premium_mf_harga.png', dpi=300)
    plt.close()

def plot_results_premium():
    df = pd.read_excel('restoran.xlsx')
    df['score'] = df.apply(lambda row: get_kelayakan_score(row['Pelayanan'], row['harga']), axis=1)

    # 3. Premium Scatter Plot
    fig, ax = plt.subplots(figsize=(12, 7))
    sc = ax.scatter(df['Pelayanan'], df['harga'], c=df['score'], cmap='magma', s=120, edgecolors='none', alpha=0.7)
    cbar = plt.colorbar(sc)
    cbar.set_label('Fuzzy Eligibility Score', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    # Highlight top 5 with glow effect
    top_5 = df.sort_values(by=['score', 'Pelayanan'], ascending=[False, False]).head(5)
    ax.scatter(top_5['Pelayanan'], top_5['harga'], color='#00E676', s=250, marker='*', label='Top 5 Selection', edgecolors='white', linewidth=1)
    
    for i, row in top_5.iterrows():
        ax.annotate(f"ID:{row['id Pelanggan']}", (row['Pelayanan'], row['harga']), 
                    xytext=(8,8), textcoords='offset points', fontsize=9, fontweight='bold', color='#69F0AE')

    ax.set_title('Restaurant Distribution: Service vs Price', fontsize=18, pad=25, fontweight='bold', color='white')
    ax.set_xlabel('Service Quality', fontsize=13)
    ax.set_ylabel('Price (IDR)', fontsize=13)
    ax.legend(facecolor='#1E1E1E', edgecolor='#444444')
    ax.grid(True, alpha=0.1)
    
    plt.tight_layout()
    plt.savefig('premium_distribution.png', dpi=300)
    plt.close()

    # 4. Premium Horizontal Bar Chart
    fig, ax = plt.subplots(figsize=(10, 6))
    top_5_sorted = top_5.sort_values('score', ascending=True)
    
    # Use a gradient-like color list
    colors = plt.cm.spring(np.linspace(0.3, 0.8, 5))
    bars = ax.barh(top_5_sorted['id Pelanggan'].astype(str), top_5_sorted['score'], color=colors, height=0.6)
    
    ax.set_title('Top 5 Recommended Restaurants', fontsize=18, pad=25, fontweight='bold', color='white')
    ax.set_xlabel('Eligibility Score', fontsize=13)
    ax.set_ylabel('Restaurant ID', fontsize=13)
    ax.set_xlim(0, 110)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2, f'{width:.2f}', 
                va='center', fontweight='bold', color='#69F0AE')

    # Remove spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('premium_top5_ranking.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    print("Generating Premium Visualizations...")
    plot_membership_premium()
    plot_results_premium()
    print("Success! Premium visualizations saved with 'premium_' prefix.")
