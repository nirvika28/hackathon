window.onload = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/category-monthly-summary");
      const data = await response.json();
  
      if (data.error) {
        console.error("Not enough data to display the chart.");
        return;
      }
  
      const categories = data.summary.map(item => item.category);
      const previousData = data.summary.map(item => item.previous);
      const currentData = data.summary.map(item => item.current);
      const colors = data.summary.map(item => item.color);
  
      const ctx = document.getElementById('spendingChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: categories,
          datasets: [
            {
              label: `Previous (${data.previous_month})`,
              data: previousData,
              backgroundColor: 'rgba(100, 149, 237, 0.7)' // light blue
            },
            {
              label: `Current (${data.current_month})`,
              data: currentData,
              backgroundColor: colors
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Category-wise Monthly Spending'
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  