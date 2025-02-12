export interface DocResponse {
    success: boolean;
    status: number;
    id?: string;
    type: number;
    errors?: { [key: string]: string };
}

