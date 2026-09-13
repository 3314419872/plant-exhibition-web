const { createApp, ref, computed } = Vue;

const plants = [
  {
    id: 1,
    name: "绿萝",
    scientific_name: "Epipremnum aureum",
    category: "观叶植物",
    description: "常见室内观叶植物，耐阴性强，适合水培或土培。",
    color: "linear-gradient(135deg, #3e8e5a, #7ec98f)",
    signature: [0.21, 0.42, 0.37],
  },
  {
    id: 2,
    name: "吊兰",
    scientific_name: "Chlorophytum comosum",
    category: "观叶植物",
    description: "叶片细长，适应性强，常用于室内净化空气。",
    color: "linear-gradient(135deg, #4aa96c, #c8e6a0)",
    signature: [0.28, 0.43, 0.29],
  },
  {
    id: 3,
    name: "仙人掌",
    scientific_name: "Opuntia dillenii",
    category: "多肉植物",
    description: "耐旱植物，茎干肉质，适合阳光充足的环境。",
    color: "linear-gradient(135deg, #5e8c61, #d9d27e)",
    signature: [0.34, 0.36, 0.30],
  },
  {
    id: 4,
    name: "常春藤",
    scientific_name: "Hedera nepalensis",
    category: "攀援植物",
    description: "攀援植物，可用于垂直绿化。",
    color: "linear-gradient(135deg, #2d6a4f, #95d5b2)",
    signature: [0.18, 0.38, 0.44],
  },
  {
    id: 5,
    name: "龟背竹",
    scientific_name: "Monstera deliciosa",
    category: "观叶植物",
    description: "叶片具有独特裂纹，是常见室内大型观叶植物。",
    color: "linear-gradient(135deg, #35745f, #a8d5ba)",
    signature: [0.20, 0.40, 0.40],
  },
];

createApp({
  setup() {
    const tab = ref("home");
    const query = ref("");
    const selectedPlant = ref(null);
    const identifyLoading = ref(false);
    const identifyError = ref("");
    const identifyResults = ref([]);

    const filteredPlants = computed(() => {
      const keyword = query.value.trim().toLowerCase();
      if (!keyword) return plants;
      return plants.filter(plant =>
        [plant.name, plant.scientific_name, plant.description]
          .join(" ")
          .toLowerCase()
          .includes(keyword)
      );
    });

    function searchPlants() {
      if (filteredPlants.value.length === 0) {
        identifyError.value = "";
      }
    }

    function extractSignature(image) {
      const canvas = document.createElement("canvas");
      const size = 96;
      canvas.width = size;
      canvas.height = size;
      const context = canvas.getContext("2d");
      context.drawImage(image, 0, 0, size, size);
      const data = context.getImageData(0, 0, size, size).data;

      let red = 0;
      let green = 0;
      let blue = 0;
      const pixels = data.length / 4;
      for (let index = 0; index < data.length; index += 4) {
        red += data[index];
        green += data[index + 1];
        blue += data[index + 2];
      }
      return [red / pixels / 255, green / pixels / 255, blue / pixels / 255];
    }

    function similarity(left, right) {
      const delta = left.map((value, index) => value - right[index]);
      const distance = Math.sqrt(delta.reduce((sum, value) => sum + value * value, 0));
      return Math.max(0, 1 - distance / Math.sqrt(3));
    }

    function handleUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      identifyLoading.value = true;
      identifyError.value = "";
      identifyResults.value = [];

      const reader = new FileReader();
      reader.onload = () => {
        const image = new Image();
        image.onload = () => {
          const signature = extractSignature(image);
          identifyResults.value = plants
            .map(plant => ({ plant, score: similarity(signature, plant.signature) }))
            .sort((left, right) => right.score - left.score)
            .slice(0, 5);
          identifyLoading.value = false;
        };
        image.onerror = () => {
          identifyError.value = "图片解析失败";
          identifyLoading.value = false;
        };
        image.src = reader.result;
      };
      reader.readAsDataURL(file);
    }

    return {
      tab,
      query,
      selectedPlant,
      identifyLoading,
      identifyError,
      identifyResults,
      filteredPlants,
      searchPlants,
      handleUpload,
    };
  },
}).mount("#app");
