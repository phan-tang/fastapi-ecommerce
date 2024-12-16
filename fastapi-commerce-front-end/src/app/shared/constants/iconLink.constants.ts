import { IconLink } from "../interfaces/app.interfaces";

const appSvgItems: IconLink = {
    name: 'angular',
    iconLink: 'angular',
    link: '/'
};

const discountSvgItem: IconLink = {
    name: 'product-discount-tag',
    iconLink: 'label'
};

const firstPaginatorSvgItem: IconLink = {
    name: 'paginator-first-page',
    iconLink: 'first_page'
};

const lastPaginatorSvgItem: IconLink = {
    name: 'paginator-last-page',
    iconLink: 'last_page'
};

const forwardPaginatorSvgItem: IconLink = {
    name: 'paginator-arrow-forward',
    iconLink: 'arrow_forward'
};

const backPaginatorSvgItem: IconLink = {
    name: 'paginator-arrow-back',
    iconLink: 'arrow_back'
};

const addToCartSvgItem: IconLink = {
    name: 'product-card-add-cart',
    iconLink: 'add_shopping_cart',
    title: "ADD TO CART"
};

const footerSvgItems: IconLink[] = [
    {
        name: 'facebook',
        iconLink: 'facebook',
        link: 'https://vi-vn.facebook.com/'
    },
    {
        name: 'instagram',
        iconLink: 'instagram',
        link: 'https://www.instagram.com/'
    },
    {
        name: 'twitter',
        iconLink: 'twitter',
        link: 'https://twitter.com/'
    }
];

const navItems: IconLink[] = [
    {
        name: "product-nav-item",
        iconLink: 'category',
        link: '/products',
        title: "Products",
    },
    {
        name: "cart-nav-item",
        iconLink: 'cart',
        link: '/cart',
        title: "Cart",
        badge: 1
    },
    {
        name: 'contact-nav-item',
        iconLink: 'contact',
        link: '/contact',
        title: "Contact",
    }
];

const starFillIcon = 'star_fill';
const starHalfIcon = 'star_half';
const starEmptyIcon = 'star_empty';

export {
    navItems,
    footerSvgItems,
    appSvgItems,
    starFillIcon,
    starHalfIcon,
    starEmptyIcon,
    addToCartSvgItem,
    discountSvgItem,
    firstPaginatorSvgItem,
    lastPaginatorSvgItem,
    backPaginatorSvgItem,
    forwardPaginatorSvgItem
}