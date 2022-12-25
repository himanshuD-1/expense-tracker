const onclickExpenseSummary = document.querySelector(".expense")

const typeData = ['pie','bar','doughnut','polarArea']



let chartType = Math.floor(Math.random()*typeData.length);


console.log(chartType)


const renderChart = (data, labels) => {
  var ctx = document.getElementById("myChart").getContext("2d");
  var myChart = new Chart(ctx, {
    type: typeData[chartType],
    data: {
      labels: labels,
      datasets: [
        {
          label: "6 months of expenses",
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255,99,132,1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      title: {
        display: true,
        text: "Expenses per Category",
      },
    },
  });
};

const getChartData = () => {
  fetch("/expense-category-summary")
    .then((res) => res.json())
    .then((results) => {
      const category_data = results.expense_category_data;
      console.log("data :", category_data);
      const [data, labels] = [
        Object.values(category_data),
        Object.keys(category_data),
      ];
      console.log(data, labels);
      renderChart(data, labels);
    });
};

document.onload = getChartData();
