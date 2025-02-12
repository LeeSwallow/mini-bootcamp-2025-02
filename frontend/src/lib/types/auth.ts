export interface AuthResponse {
    success: boolean;
    status: number;
    token?: string;
    user_id?: string;
    errors?: { [key: string]: string };

}

export interface LoginRequest {
    login_id: string;
    password: string;
}

export interface SignupRequest {
    email: string;
    login_id: string;
    username: string;
    password1: string;
    password2: string;
}
