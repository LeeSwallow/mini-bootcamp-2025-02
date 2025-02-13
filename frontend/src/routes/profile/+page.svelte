<script context="module" lang="ts">
  export { load } from "./+page";
</script>

<script lang="ts">
  import type { User } from "$lib/types/user_model";
  import type { ModalSettings } from "@skeletonlabs/skeleton";
  import { getModalStore } from "@skeletonlabs/skeleton";
  import { ConfirmEditProfileModal } from "$lib/components/modal";
  import { token } from "$lib/stores/token.js";
  import { user_id } from "$lib/stores/user.js";
  import { convertError } from "$lib/service/errors";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import { goto } from "$app/navigation";
  import { get } from "svelte/store";

  const modalStore = getModalStore();
  export let data: { user: User };
  const { user } = data;
  const field: { login_id?: string; username?: string; password?: string } = {
    login_id: user.login_id,
    username: user.username,
  };
  const fieldError: Record<string, string> = {
    all: "",
    email: "",
    login_id: "",
    username: "",
    password: "",
  };
  $: serverErrorCheck = fieldError.all.length > 0;
  $: userIdErrorCheck = fieldError.login_id.length > 0;
  $: usernameErrorCheck = fieldError.username.length > 0;
  $: passwordErrorCheck = fieldError.password.length > 0;

  const handleSubmitEdit = async (event: Event) => {
    const formData = { ...field };
    if (field.login_id === user.login_id) delete formData.login_id;
    if (field.password === "") delete formData.password;

    const res = await fetch("/api/put/users/self", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${get(token)}`,
      },
      body: JSON.stringify(formData),
    });
    const body = await res.json();
    if (res.ok) {
      token.set(body.access_token);
      user_id.set(body.sub);
      modalStore.trigger(ConfirmEditProfileModal);
    } else {
      const error = convertError(body.detail);
      for (const key of Object.keys(fieldError)) {
        fieldError[key] = error[key] ? error[key].msg : "";
      }
    }
  };
  const handleSubmitDelete = async () => {
    return fetch("/api/delete/users/self", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${get(token)}`,
      },
      body: JSON.stringify({ login_id: field.login_id }),
    });
  };

  const ClickDeleteModal: ModalSettings = {
    type: "confirm",
    title: "회원 탈퇴",
    body: "정말로 탈퇴하시겠습니까?",
    buttonTextConfirm: "탈퇴",
    buttonTextCancel: "취소",
    response: (response: boolean) => {
      if (response) {
        handleSubmitDelete().then((res) => {
          if (res.ok) {
            token.set(null);
            user_id.set(null);
            goto("/");
          } else {
            res.json().then((body) => {
              const error = convertError(body.detail);
              for (const key of Object.keys(fieldError)) {
                fieldError[key] = error[key] ? error[key].msg : "";
              }
            });
          }
        });
      }
    },
  };

  const onClickDelete = () => {
    modalStore.trigger(ClickDeleteModal);
  };
  let visible = false;
  onMount(() => {
    visible = true;
  });
</script>

{#if visible}
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
          회원 정보 수정
        </h1>
        <form
          class="space-y-4 md:space-y-6"
          method="post"
          on:submit|preventDefault={handleSubmitEdit}
        >
          {#if serverErrorCheck}
            <div class="text-red-500 dark:text-red-400">
              {fieldError.all}
            </div>
          {/if}

          <div>
            <label
              for="login_id"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >사용자 ID</label
            >
            <input
              type="input"
              name="login_id"
              id="login_id"
              bind:value={field.login_id}
              class="input block w-full p-2.5"
            />
          </div>

          {#if userIdErrorCheck && !serverErrorCheck}
            <div class="text-red-500 dark:text-red-400">
              {fieldError.login_id}
            </div>
          {/if}

          <div>
            <label
              for="username"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >사용자 이름</label
            >
            <input
              type="input"
              name="username"
              id="username"
              bind:value={field.username}
              class="input block w-full p-2.5"
            />
          </div>
          {#if usernameErrorCheck && !serverErrorCheck}
            <div class="text-red-500 dark:text-red-400">
              {fieldError.username}
            </div>
          {/if}

          <div>
            <label
              for="password"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >비밀번호</label
            >
            <input
              type="password"
              name="password"
              id="password"
              bind:value={field.password}
              placeholder="••••••••"
              class="input block w-full p-2.5"
            />
          </div>

          {#if passwordErrorCheck && !serverErrorCheck}
            <div class="text-red-500 dark:text-red-400">
              {fieldError.password}
            </div>
          {/if}

          <div class="space-y-4 md:space-y-6"></div>
          <button
            on:click={handleSubmitEdit}
            class="btn variant-ghost-primary w-full font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >수정 완료</button
          >
          <button
            on:click={onClickDelete}
            class="btn variant-ghost-error w-full font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >회원 탈퇴</button
          >
        </form>
      </div>
    </div>
  </section>
{/if}

<style>
</style>
