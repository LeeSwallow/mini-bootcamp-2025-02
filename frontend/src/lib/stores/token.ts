import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const storedToken = browser ? localStorage.getItem('access-token') : null;
export const token = writable<string | null>(storedToken);

export const isLoggedIn = writable<boolean>(storedToken != null);

if (browser) {
  token.subscribe((value) => {
    if (value) {
      localStorage.setItem('access-token', value);
      isLoggedIn.set(true);
    } else {
      localStorage.removeItem('access-token');
      isLoggedIn.set(false);
    }
  });
}


