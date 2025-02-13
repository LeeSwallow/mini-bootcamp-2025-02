<script lang="ts">
  import { goto } from "$app/navigation";
  import { token } from "$lib/stores/token";
  import { user_id } from "$lib/stores/user";
  import { convertError } from "$lib/service/errors";
  import { fade } from "svelte/transition";

  const fields = {
    login_id: "",
    password: "",
  };

  const fieldErrors: { [key: string]: string } = {
    all: "",
    login_id: "",
    password: "",
  };
  $: serverError = fieldErrors.all ? true : false;
  $: userIdError = fieldErrors.login_id ? true : false;
  $: passwordError = fieldErrors.password ? true : false;

  const handleSubmit = async (event: Event) => {
    const res = await fetch("/api/post/json/auth/signin", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(fields),
    });
    const body = await res.json();
    if (res.ok) {
      token.set(body.access_token);
      user_id.set(body.sub);
      goto("/");
    } else {
      const error = convertError(body.detail);
      for (const key of Object.keys(fieldErrors)) {
        fieldErrors[key] = error[key] ? error[key].msg : "";
      }
    }
  };
</script>

<section
  transition:fade={{ duration: 100 }}
  class="flex flex-col items-center justify-center px-6 py-8 mx-auto"
>
  <div
    class="w-full bg-white rounded-lg shadow dark:border sm:max-w-md xl:p-0 dark:bg-surface-800 dark:border-gray-700"
  >
    <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
      <h1
        class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
      >
        로그인
      </h1>
      <!-- 폼 시작 -->
      <form
        class="space-y-4 md:space-y-6"
        method="post"
        on:submit|preventDefault={handleSubmit}
      >
        {#if serverError}
          <div class="text-red-500 dark:text-red-400">
            {fieldErrors.all}
          </div>
        {/if}

        <div>
          <label
            for="login_id"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >사용자 ID</label
          >
          <input
            bind:value={fields.login_id}
            type="input"
            name="login_id"
            id="login_id"
            class="input block w-full p-2.5"
            required
          />
        </div>
        {#if !serverError && userIdError}
          <div class="text-red-500 dark:text-red-400">
            {fieldErrors.login_id}
          </div>
        {/if}
        <label
          for="password"
          class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >비밀번호</label
        >
        <input
          bind:value={fields.password}
          type="password"
          name="password"
          id="password"
          placeholder="••••••••"
          class="input block w-full p-2.5"
          required
        />
        <div class="space-y-4 md:space-y-6">
          {#if !serverError && passwordError}
            <div class="text-red-500 dark:text-red-400">
              {fieldErrors.password}
            </div>
          {/if}
        </div>
        <button
          type="submit"
          class="btn btn variant-ghost-primary w-full font-medium rounded-lg text-sm px-5 py-2.5 text-center"
          >로그인</button
        >
        <p class="text-sm font-light text-surface-500 dark:text-surface-400">
          계정이 존재하지 않나요? <a
            href="/signup"
            class="font-medium text-primary-600 hover:underline dark:text-primary-500 px-5"
            >회원가입</a
          >
        </p>
      </form>
    </div>
  </div>
</section>

<style lang="postcss">
</style>
