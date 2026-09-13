const { createApp, ref, onMounted } = Vue;

createApp({
  setup() {
    const tab = ref("home");
    const plants = ref([]);
    const query = ref("");
    const selectedPlant = ref(null);
    const identifyLoading = ref(false);
    const identifyError = ref("");
    const identifyResults = ref([]);

    async function fetchPlants() {
      const params = new URLSearchParams();
      if (query.value.trim()) {
        params.set("q", query.value.trim());
      }

      const response = await fetch(`/api/plants?${params.toString()}`);
      plants.value = await response.json();
    }

    async function handleUpload(event) {
      const file = event.target.files[0];
      if (!file) {
        return;
      }

      identifyLoading.value = true;
      identifyError.value = "";
      identifyResults.value = [];

      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("/api/identify", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const data = await response.json();
          identifyError.value = data.detail || "识别失败";
        } else {
          identifyResults.value = await response.json();
        }
      } catch (error) {
        identifyError.value = "网络请求失败";
      } finally {
        identifyLoading.value = false;
      }
    }

    onMounted(fetchPlants);

    return {
      tab,
      plants,
      query,
      selectedPlant,
      identifyLoading,
      identifyError,
      identifyResults,
      fetchPlants,
      handleUpload,
    };
  },
}).mount("#app");
