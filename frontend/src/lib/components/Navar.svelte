<script lang="ts">
  import { goto } from "$app/navigation";
  import { AppBar } from "@skeletonlabs/skeleton";
  import { token, isLoggedIn } from "$lib/stores/token";
  import { user_id } from "$lib/stores/user";
  import { get } from "svelte/store";
  import { browser } from "$app/environment";

  if ( browser ) {
    token.set(localStorage.getItem("token"));
    user_id.set(localStorage.getItem("user_id"));
  }
  isLoggedIn.set(get(token) !== null);

  token.subscribe((value) => {
    isLoggedIn.set(value !== null);
  });

  const handleLogout = () => {
    token.set(null);
    user_id.set(null);
    goto("/");
  };
</script>

<AppBar class="mb-4">
  <svelte:fragment slot="lead">
    <strong class="text-xl font-bold uppercase">
      <a href="/"> My PDF Summarizer </a>
    </strong>
  </svelte:fragment>
  <svelte:fragment slot="trail">
    {#if $isLoggedIn}
      <button
        class="btn font-bold variant-ghost-surface"
        on:click={() => handleLogout()}>로그아웃</button
      >
      <button
        class="btn font-bold variant-ghost-surface"
        on:click={() => goto("/hub")}>My HUB</button
      >
    {:else}
      <button
        class="btn font-bold variant-ghost-surface"
        on:click={() => goto("/login")}>로그인</button
      >
      <button
        class="btn font-bold variant-ghost-surface"
        on:click={() => goto("/signup")}>회원가입</button
      >
    {/if}
  </svelte:fragment>
</AppBar>
