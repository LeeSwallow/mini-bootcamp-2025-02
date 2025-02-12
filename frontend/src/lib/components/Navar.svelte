<script lang="ts">
    import { goto } from '$app/navigation';
    import { AppBar } from '@skeletonlabs/skeleton';
    import { token } from '$lib/stores/token'; 
    import { user_id } from '$lib/stores/user';
    import { get } from 'svelte/store';
    let isLoggedIn:boolean = get(token) !== null;
    token.subscribe(value => {
        isLoggedIn = value !== null;
    });
    const handleLogout = () => { token.set(null); user_id.set(null); goto('/'); };
</script>
<AppBar class="mb-4">
    <svelte:fragment slot="lead">
        <strong class="text-xl uppercase">
            My PDF Summarizer
        </strong>
    </svelte:fragment>
    <svelte:fragment slot="trail">
        <button class="btn variant-ghost-surface" on:click={() => goto('/')}>홈</button>
        {#if isLoggedIn}
            <button class="btn variant-ghost-surface" on:click={handleLogout}>로그아웃</button>
            <button class="btn variant-ghost-surface" on:click={() => goto('/hub')}>마이페이지</button>
        {:else}
            <button class="btn variant-ghost-surface" on:click={() => goto('/login')}>로그인</button>
            <button class="btn variant-ghost-surface" on:click={() => goto('/signup')}>회원가입</button>
        {/if}
    </svelte:fragment>
</AppBar>