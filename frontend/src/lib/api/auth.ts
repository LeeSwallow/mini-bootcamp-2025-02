import type { AuthResponse, LoginRequest, SignupRequest } from '$lib/types/auth';
import { convertErrorFormat } from '$lib/api/default';
import { resolveConfig } from 'prettier';

function fetchBackend(url: string, body: LoginRequest | SignupRequest) : Promise<AuthResponse> {
    let isSuccessful = false;
    let status = 0;
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }).then(res => { 
        console.log(res);

        isSuccessful = res.ok; 
        status = res.status;
        return res.json();
    }).then(data => {
        console.log(data);

        if (isSuccessful) {
            return { success: true, status: status, token: data.access_token, user_id: data.sub };
        } else {
            const errors = convertErrorFormat(data.detail);
            return { success: false, status: status, errors: errors };
        }
    }).catch(err => {
        return {
            success: false,
            status: 500,
            errors: { all: '서버에 내부적인 문제가 발생했습니다. ' }
        };
    });
}

export const login = (base_url: string , req: LoginRequest) : Promise<AuthResponse> => {
    return fetchBackend(`${base_url}/auth/signin`, req);
}

export const signup = (base_url: string, req: SignupRequest) : Promise<AuthResponse> => {
    return fetchBackend(`${base_url}/auth/signup`, req)
       .then(res => {
            if (!res.success && res.errors && res.errors.body) {
                res.errors.password2 = res.errors.body;
                delete res.errors.body;
            }
            return res;
       });
}
