/**
 * NovaGear — UI builders
 */
const NovaGearUI = {
  createProductCard(product) {
    const inWishlist = NovaGear.getWishlist().includes(product.id);
    const priceOldHtml = product.priceOld
      ? `<span class="product-card__price-old">${NovaGear.formatPrice(product.priceOld)}</span>`
      : "";

    const article = document.createElement("article");
    article.className = "product-card";
    article.dataset.productId = product.id;
    article.innerHTML = `
      <div class="product-card__media">
        <div class="product-card__img product-card__img--placeholder ${product.imageClass}" role="img" aria-label="${product.name}"></div>
        <button type="button" class="product-card__wishlist ${inWishlist ? "is-active" : ""}"
          data-wishlist-id="${product.id}" aria-label="Add to wishlist" aria-pressed="${inWishlist}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>
        </button>
      </div>
      <div class="product-card__body">
        <span class="product-card__category">${product.category}</span>
        <h3 class="product-card__title"><a href="catalog.html">${product.name}</a></h3>
        <div class="product-card__rating">
          <span class="product-card__stars" aria-label="Rating ${product.rating} out of 5">${NovaGear.renderStars(product.rating)}</span>
          <span class="product-card__reviews">(${product.reviews})</span>
        </div>
        <div class="product-card__footer">
          <div>
            <span class="product-card__price">${NovaGear.formatPrice(product.price)}</span>
            ${priceOldHtml}
          </div>
          <button type="button" class="btn btn--primary btn--sm" data-add-cart="${product.id}">Add to cart</button>
        </div>
      </div>
    `;
    return article;
  },

  renderProductGrid(container, products) {
    if (!container) return;
    container.innerHTML = "";
    if (!products.length) {
      container.innerHTML = `<p class="empty-state">No products found. Try adjusting filters.</p>`;
      return;
    }
    products.forEach((product) => {
      container.appendChild(this.createProductCard(product));
    });
  },
};
