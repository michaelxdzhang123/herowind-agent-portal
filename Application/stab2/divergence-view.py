import matplotlib.pyplot as plt
import pandas as pd
import os

def main():
    """读取发散分析 CSV 数据并绘制时间-数值曲线，结果保存为 PNG 图片。"""
    # Check if the CSV file exists
    csv_file = './divergence/divergence-view.csv'
    if not os.path.exists(csv_file):
        print(f"Error: File {csv_file} not found!")
        return
    
    try:
        # Read the CSV file
        data1 = pd.read_csv(csv_file)
        print(f"Data loaded successfully. Shape: {data1.shape}")
        print(f"Columns: {list(data1.columns)}")
        
        # Check if required columns exist
        if 'time' not in data1.columns:
            print("Error: 'time' column not found!")
            print(f"Available columns: {list(data1.columns)}")
            return
            
        # Use 'Value' column for y-axis
        y_column = 'Value'
        if 'Value' not in data1.columns:
            print("Error: 'Value' column not found!")
            print(f"Available columns: {list(data1.columns)}")
            return
        
        print(f"Using x-axis: time, y-axis: {y_column}")
        
        # Convert time to numeric if needed
        data1['time'] = pd.to_numeric(data1['time'], errors='coerce')
        
        # Remove any NaN values
        clean_data = data1[['time', y_column]].dropna()
        
        if len(clean_data) == 0:
            print("Error: No valid data points after cleaning!")
            return
            
        print(f"Plotting {len(clean_data)} data points")
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        plt.plot(clean_data['time'], clean_data[y_column], label=f'Data ({y_column})', linewidth=2)
        
        plt.xlabel('Time (s)')
        plt.ylabel(f'{y_column}')
        plt.title('Load Divergence Analysis')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save the plot
        plt.savefig('divergence_plot.png', dpi=300, bbox_inches='tight')
        print("Plot saved as 'divergence_plot.png'")
        
        # Show the plot
        plt.show()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please check your CSV file format and column names.")

if __name__ == "__main__":
    main()