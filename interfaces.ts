export interface Record {
    id: number;
    category_id: number;
    category_name: string;
    datetime: string;
    from: string;
    type: string;
    price: number;
    memo: string;
}

export interface Category {
    category_id: number;
    category_name: string;
}

export interface SummaryOne {
    category_id: number;
    category_name: string;
    price: number[]; // 4,5,6,7,8,9,10,11,12,1,2,3月の額
    total: number;
}
