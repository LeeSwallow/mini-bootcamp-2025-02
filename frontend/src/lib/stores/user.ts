import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const user_init = browser ? localStorage.getItem('user') : null;

export const user_id = writable<string | null>(user_init);
if (browser) {
    user_id.subscribe((value: string | null) => {
        if (value) {
            localStorage.setItem('user', value);
        } else {
            localStorage.removeItem('user');
        }
    });
}