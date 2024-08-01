class Pagination {
  #buttonsToShow = 5;
  #render = [];
  #pageSize = 0; // how many pages exist
  #currentPage = 0;
  #nextPage;
  #previousPage;

  setPageSize(size) {
    if (size >= 1) {
      this.#pageSize = size;
      this.#currentPage = 1;
    }

    if (this.#pageSize > 0 && this.#pageSize <= 5) {
      for (let i = 1; i <= this.#pageSize; i++) {
        this.#render.push(i);
      }
    }
  }
  setCurrentPage(current) {
    if (this.#pageSize >= 1 && current >= 1 && current <= this.#pageSize) {
      this.#currentPage = current;
      if (current < this.#pageSize) this.#nextPage = current + 1;
      if (current > 1) this.#previousPage = current - 1;
    }
  }
  get() {
    return {
      render: this.#render,
      current: this.#currentPage,
      next: this.#nextPage,
      prev: this.#previousPage,
    };
  }
}

const pagination = new Pagination();
pagination.setPageSize(3);
pagination.setCurrentPage(2);
console.log(pagination.get());

module.exports = Pagination;
