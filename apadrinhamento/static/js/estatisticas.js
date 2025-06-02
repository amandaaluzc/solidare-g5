 document.addEventListener("DOMContentLoaded", () => {
        const labelsData = JSON.parse(document.getElementById("chart-labels").textContent);
        const chartData = JSON.parse(document.getElementById("chart-data").textContent);
        const ctx = document.getElementById("myChart").getContext("2d");

        Chart.register(ChartDataLabels);

        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: labelsData,
                datasets: [{
                    data: chartData,
                    backgroundColor: ["red", "blue"]
                }]
            },
            options: {
                plugins: {
                    datalabels: {
                        formatter: (value, context) => value  + " crianças",
                        color: '#fff'
                    },

                    title: {
                        display: true,
                        text: 'Relação entre número de total de afilhados X afilhados apadrinhados', 
                        font: {
                                size: 20, 
                        },
                        align: 'center'
                        
                        },
                }
            }
        });
    });