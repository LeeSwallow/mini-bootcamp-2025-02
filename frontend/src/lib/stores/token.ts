import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface Local {
    token: string | null;
    isLogin: boolean;
}

export const local = writable<Local>({token:null, isLogin:false});

export function setToken(token: string) {
    if ( browser ) {
        localStorage.setItem('access-token', token);
        local.set({token: token, isLogin: true});
    }
}

export function removeToken() {
    if ( browser ) {
        localStorage.removeItem('access-token');
        local.set({token: null, isLogin: false});
    }
}

export function getToken() {
    if ( browser ) {
        let token: string | null = localStorage.getItem('access-token');
        let isLogin: boolean = (token !== null) ? true : false;
        return {
            token: token,
            isLogin: isLogin
        };
    } else {
        return {token: null, isLogin: false};
    }
}
