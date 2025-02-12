export interface DocResponse {
    success: boolean;
    id?: string;
}

export interface DocumentList {
    documents: Array<Document>;
    total: number;
}

export interface Document {
    id: string;
    title: string;
    num_page: number;
    created_at: string;
    thumbnail_path?: string;
}

