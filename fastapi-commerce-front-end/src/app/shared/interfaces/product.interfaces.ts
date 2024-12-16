export interface ProductData {
    id: string;
    brand_name: string;
    category_name: string;
    product_name: string;
    description: string;
    price: number;
    quantity: number;
    average_rating: number;
    discount_value?: number;
    discount_percentage?: number;
    discount_type?: string;
    final_price: number;
    main_image_link?: string;
    image_links?: string;
    product_status?: string;
    sub_categories: []
}

export interface ProductListData {
    data: ProductData[];
    total_items: number;
}