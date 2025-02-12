import type { Actions } from '@sveltejs/kit';
import { setToken } from '$lib/stores/token';
import { login } from '$lib/api/backend/auth';
import type { AuthResponse, LoginRequest, SignupRequest } from '$lib/types/auth';
import { BACKEND_URL } from '$env/static/private';


export const actions: Actions = {
    default: async (event) => {
        const formData = await event.request.formData();
        const LoginRequest: LoginRequest = {
            login_id: formData.get('login_id') as string,
            password: formData.get('password') as string,
        };
        const response: AuthResponse = await login(BACKEND_URL, LoginRequest);
        console.log(response);
        if (response.success) {

            return {
                status: 200,
                body : {
                    success: response.success,
                    token: response.token
                }   
            }
        } else {
            return {
                status: response.status,
                body: {
                    errors: response.errors
                }
            }
        }
    }
};
