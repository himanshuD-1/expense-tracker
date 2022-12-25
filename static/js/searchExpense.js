const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appOutput = document.querySelector(".app-output");
const paginationContainer = document.querySelector(".pagination-container");

const tbody = document.querySelector(".table-body");

tableOutput.style.display = "none";

searchField.addEventListener("keyup", (e) => {
  const searchVal = e.target.value;

 if(searchVal.trim().length > 0){
    paginationContainer.style.display = "none";
    tbody.innerHTML = "";
    
    fetch("/search-expenses", {
        body: JSON.stringify({ searchText: searchVal }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {   
          console.log(data);
          tableOutput.style.display = "block";
          appOutput.style.display = "none";

          if(data.length == 0){
            tableOutput.innerHTML = "No result found"
          }
          else{
            data.forEach(item => {
                tbody.innerHTML +=
                `<tr>
                <td>${item.amount}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                <td>${item.category}</td>
                <tr>`
            });
          }
        });
    }
    else{
        tableOutput.style.display = "none";
        appOutput.style.display = "block";
        paginationContainer.style.display = "block";
    }
});
