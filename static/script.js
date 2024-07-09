class App {
  constructor(name, location) {
    this.data = [];
    this.update();
  }
  async fetch() {
    const response = await fetch("/api/rentals");
    this.data = await response.json();
  }
  async update() {
    await this.fetch();
    let tbody = document.querySelector('#app > table > tbody');
    for (const rental of this.data) {
      for (const reserv of rental.reservations) {
        let row = document.createElement('tr');
        row.innerHTML = `
            <td>${rental.name}-${rental.id}</td>
            <td>${reserv.id}</td>
            <td>${reserv.checkin}</td>
            <td>${reserv.checkout}</td>
            <td>${reserv.previous == null? '-': reserv.previous}</td>
        `;
        tbody.appendChild(row);
      }
    }
  }
}

new App();

