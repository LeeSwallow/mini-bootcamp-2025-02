import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface Auth {
    token: string | null;
    isLogin: boolean;
}

export const auth = writable<Auth>({token:null, isLogin:false});

export function setAuth(token: string) {
    if ( browser ) {
        localStorage.setItem('access-token', token);
        localStorage.setItem('is-login', 'true');
        auth.set({token, isLogin: true});
    }
}

export function removeAuth() {
    if ( browser ) {
        localStorage.removeItem('access-token');
        localStorage.removeItem('is-login');
        auth.set({token: null, isLogin: false});
    }
}

export function getAuth() {
    if ( browser ) {
        console.log("auth is called");
        return {
            token: localStorage.getItem('access-token'),
            isLogin: localStorage.getItem('is-login') === 'true'
        };
    } else {
        return {token: null, isLogin: false};
    }
}
