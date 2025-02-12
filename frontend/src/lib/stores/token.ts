import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const storedToken = browser ? localStorage.getItem('access-token') : null;
export const token = writable<string | null>(storedToken);
export const isLoggedIn = token.subscribe(value => value !== null);
if (browser) {
    token.subscribe((value) => {
        if (value) {
            console.log('Token Setted:', value);    
            localStorage.setItem('access-token', value);
        } else {
            console.log('Token Removed');
            localStorage.removeItem('access-token');
        }
    });
}


