<script lang="ts">
    import { goto } from '$app/navigation';
    import { AppBar } from '@skeletonlabs/skeleton';
    import { local, removeToken, getToken } from '$lib/stores/token';   

    let isLogin = getToken().isLogin;
    local.subscribe(value => {
        isLogin = value.isLogin;
    });
    async function handleLogout() {
        if (isLogin) { removeToken(); ;goto('/'); };
    }
</script>

<AppBar class="mb-4">
    <svelte:fragment slot="lead">
        <strong class="text-xl uppercase">
            My PDF Summarizer
        </strong>
    </svelte:fragment>
    <svelte:fragment slot="trail">
        <button class="btn variant-ghost-surface" on:click={() => goto('/')}>홈</button>
        {#if isLogin}
            <button class="btn variant-ghost-surface" on:click={handleLogout}>로그아웃</button>
            <button class="btn variant-ghost-surface" on:click={() => goto('/hub')}>마이페이지</button>
        {:else}
            <button class="btn variant-ghost-surface" on:click={() => goto('/login')}>로그인</button>
            <button class="btn variant-ghost-surface" on:click={() => goto('/signup')}>회원가입</button>
        {/if}
    </svelte:fragment>
</AppBar>