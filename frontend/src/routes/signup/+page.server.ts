import type { Actions } from '@sveltejs/kit';
import { signup } from '$lib/api/auth';
import type { AuthResponse, SignupRequest } from '$lib/types/auth';
import { BACKEND_URL } from '$env/static/private';

export const actions: Actions = {
    default: async (event) => {
        const formData = await event.request.formData();
        const signupReq: SignupRequest = {
            login_id: formData.get('login_id') as string,
            email: formData.get('email') as string,
            username: formData.get('username') as string,
            password1: formData.get('password1') as string,
            password2: formData.get('password2') as string,
        };
        const response: AuthResponse = await signup(BACKEND_URL, signupReq);
        if (response.success) {
            return {
                status: 200,
                body : {
                    success: response.success,
                    token: response.token,
                }
            }   
        } else {
            return {
                status: response.status,
                body: {
                    success: response.success,
                    errors: response.errors
                }
            }
        }
    }
};
