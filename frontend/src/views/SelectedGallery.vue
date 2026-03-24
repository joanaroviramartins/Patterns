<template>
  <div class="container">
    <section class=section id="gallery">
      <div class="gallery-header">
        <h1 class="gallery-title">GALLERY</h1>
        <div class="search-container">
          <div class="searchTermContainer">
            <p class="bold searchTermTitle">Searched Word(s)</p>
            <div class="searchTerm">{{ searchTerm }}</div>
          </div>
          <div class="relatedWordsContainer">
            <p class="bold relatedWordsTitle">Related Words List</p>
            <div class="relatedWords">{{ relatedWords.join(", ") }}</div>
          </div>
        </div>
      </div>

      <div class="gallery-grid-container-selected">
        <div class="gallery-grid">
          <div
            v-for="(image, index) in selectedImages"
            :key="index"
            :class="['gallery-item', image.orientation, { selected: isSelected(image) }]" 
            @click="handleImageClick(image)"
          >
            <img :src="`/static/InputWorks/${image.id_imagem}`" :alt="image.id_imagem" />
            <div class="caption">
              <div @click="infoButton(image)" class="div_wordsPathGallery">info+</div> <br>
              <div class="div_infoPathGallery">
                <p>{{ searchTerm }} -> {{ image.palavras_chave[0] }} </p> <br>
                <p>Relation: {{ image.relation }}</p>
                <p>(Prob: {{ image.prob[0] }})</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="footer">
        <div class="progress">
          <div class="navigationGeneral">
            <span class="nav-circle"></span>
            <span class="nav-line"></span>
            <span class="nav-circle active" @click="readingFile"></span>
            <span class="nav-line"></span>
            <span class="nav-circle" @click="decompose"></span>
            <span class="nav-line"></span>
            <span class="nav-circle"></span>
          </div>
          <div class="navigation-namesGeneral">
            <span class="nav">GALLERY</span>
            <span class="nav active">SELECTED GALLERY</span>
            <span class="nav">UNIT DEVELOPMENT</span>
            <span class="nav ">PATTERN</span>
          </div>
        </div>
        <div class="div-arrow">
          <span id="submit">CHOOSE THE WORKS YOU WANT TO DECOMPOSE</span>
          <div class="nav-arrow" @click="decompose">▶</div>
        </div>
      </div>
    </section>

    <section class="section" id="waitingGallery" v-if="showWaitingGallery">
      <p class="galleryText">
        While I am decomposing it, take a look at what other users have done!
      </p>
      <div class="slideshow-container">
        <div
          v-for="(img, index) in waitingGalleryImages"
          :key="index"
          class="slide"
          :class="{ active: index === currentSlideIndex }"
        >
          <img
            :src="`/static/waitingGallery/${img}`"
            :alt="`Image ${index + 1}`"
            class="slide-image"
          />
        </div>
        
      </div>
      <button class="prev" @click="prevSlide">❮</button>
      <button class="next" @click="nextSlide">❯</button>

      <div class="dots">
        <span
          v-for="(img, index) in waitingGalleryImages"
          :key="index"
          class="dot"
          :class="{ active: index === currentSlideIndex }"
          @click="goToSlide(index)"
        ></span>
      </div>
    </section>

    <div v-if="showDefinitionModal" class="modal-overlay" @click.self="closeDefinitionModal">
      <div class="modal-content">
        <button class="close-x" @click="closeDefinitionModal">×</button>
        <div class="defition"> Definition </div>
        <p>{{ currentDefinition }}</p>
      </div>
    </div>

    <div v-if="showLoadingModal" class="modal-overlay">
      <div class="loading-modal-content">
        <div class="spinner"></div>
        <p>Loading definition, please wait...</p>
      </div>
    </div>
  </div>

 
</template>


<script>
import axios from 'axios';

export default {
  name: 'SelectedGallery',
  data() {
    return {
      waitingGalleryImages: [],
      searchTerm: "",
      relatedWords: [],
      selectedImages: [],
      imagensSelecionadas: [], 
      showWaitingGallery: false,
      currentSlideIndex: 0,
      showDefinitionModal: false,
      currentDefinition: "",
      showLoadingModal: false,
    };
  },
  methods: {
    async infoButton(image) {
      try {
        this.showLoadingModal = true; 
        const keyword = image.palavras_chave[0]; 
        const originail_relation = image.relation;
        const relation = typeof image.relation === 'string'
          ? image.relation.split(' ')[0]
          : (Array.isArray(image.relation) ? String(image.relation[0]).split(' ')[0] : '');
        const selectImages = this.selectedImages.map(img => img.id_imagem).join(','); 

        const response = await axios.get('http://127.0.0.1:5000/wordDefinition', {
          params: {
            keyword,
            relation,
            selectImages
          }
        });

        const definition = response.data.definition;
        image.relation = `${originail_relation}. ${definition}`;

        this.currentDefinition = definition;
        this.showDefinitionModal = true;
      } catch (error) {
        console.error('Error sending word description:', error);
      } finally {
        this.showLoadingModal = false; 
      }
    },
    closeDefinitionModal() {
      this.showDefinitionModal = false;
      this.currentDefinition = "";
    },
    isSelected(image) {
      return this.imagensSelecionadas.some(
        (item) => item.id_imagem === image.id_imagem
      );
    },
    handleImageClick(image) {
      const isSelected = this.isSelected(image);

      if (isSelected) {
        this.imagensSelecionadas = this.imagensSelecionadas.filter(
          (item) => item.id_imagem !== image.id_imagem
        );
      } else {
        this.imagensSelecionadas.push(image);
      }
    },
    decompose() {
      if (this.imagensSelecionadas.length === 0) {
        alert("You have to choose the works you want to decompose by clicking on them.");
        return;
      } else {
        this.showWaitingGallery = true;
        this.scrollToWaiting();
      }      

      axios
        .get("http://127.0.0.1:5000/decompor", {
          params: {
            searchTerm: this.searchTerm,
            semanticWords: this.relatedWords.join(", "),
            selectImages: JSON.stringify(this.imagensSelecionadas),
          },
        })
        .then((response) => {
          if (response.data.success) {
            const { semanticSearch, searchedTerm, png_files, png_files_name, decomposed_info } = response.data;

            this.$router.push({
              path: '/unit',
              query: {
                searchedTerm: JSON.stringify(searchedTerm),
                semanticSearch: JSON.stringify(semanticSearch),
                png_files: JSON.stringify(png_files),
                png_files_name: JSON.stringify(png_files_name),
                decomposed_info: JSON.stringify(decomposed_info),
              },
            });
          } else {
            console.error("Error: ", response.data.message);
          }
        })
        .catch((error) => {
          console.error("Error API:", error);
        });
    },
    scrollToWaiting() {
      this.$nextTick(() => {
        const waitingSection = document.getElementById("waitingGallery");
        if (waitingSection) {
          waitingSection.scrollIntoView({ behavior: "smooth" });
        }
      });
    },
    nextSlide() {
      this.currentSlideIndex =
        (this.currentSlideIndex + 1) % this.waitingGalleryImages.length;
    },
    prevSlide() {
      this.currentSlideIndex =
        (this.currentSlideIndex - 1 + this.waitingGalleryImages.length) %
        this.waitingGalleryImages.length;
    },
    goToSlide(index) {
      this.currentSlideIndex = index;
    },
    async fetchWaitingGallery() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/waiting-gallery');
        let images = response.data.images;

        for (let i = images.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [images[i], images[j]] = [images[j], images[i]];
        }

        this.waitingGalleryImages = images.slice(0, 10);
        
        if (this.waitingGalleryImages.length === 0) {
           this.waitingGalleryImages = ["0.svg", "1.svg", "2.svg"]; 
        }

      } catch (error) {
        console.error("Error loading waiting gallery:", error);
        this.waitingGalleryImages = ["0.svg", "1.svg"]; 
      }
    },
  },
  created() {
    const searchTerm = JSON.parse(this.$route.query.searchTerm || '');
    const relatedWords = JSON.parse(this.$route.query.relatedWords || '[]');
    const selectedImages = JSON.parse(this.$route.query.selectedImages || '[]');

    this.searchTerm = searchTerm;
    this.relatedWords = relatedWords;
    this.selectedImages = selectedImages;
  },
  mounted() {
    this.fetchWaitingGallery();
  },
};
</script>

<style scoped>

.slideshow-container {
  position: relative;
  width: 100%;
  max-width: 600px; 
  margin: 20px auto;
  overflow: hidden;
}

.slide {
  display: none;
  width: 100%;
  height: 450px; 
  position: relative;
  justify-content: center; 
  align-items: center;
}

.slide.active {
  display: flex; 
  animation: fade 0.5s;
}

.slide-image {
  max-width: 100%;
  max-height: 100%;
  width: auto;   
  height: auto;  
  object-fit: contain; 
  padding: 20px; 
}

.prev,
.next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 1.5rem;
  color: #A67E66; 
  padding: 10px 15px;
  background: none;
  border: none;
  border-radius: 50%;
  user-select: none;
  transition: background 0.3s;
  z-index: 2; 
}

.prev:hover, .next:hover {
  background: none;
  font-weight: bold;
}

.prev { left: 20%; }
.next { right: 20%; }

/* Pontos (Dots) */
.dots {
  text-align: center;
  margin-top: 15px;
}

.dot {
  height: 10px;
  width: 10px;
  margin: 0 5px;
  background-color: #ccc;
  border-radius: 50%;
  display: inline-block;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dot.active {
  background-color: #A67E66;
}

@keyframes fade {
  from {opacity: .4} 
  to {opacity: 1}
}

#waitingGallery {
  background: #F9F5EF;
  padding: 30px 20px;
}

.galleryText {
  font-size: 25px;
margin-top: 3%;
}


@media (max-width: 768px) {
  .slideshow-container {
    max-width: 90%;
  }

  .slide {
    height: 300px;
  }
  
  .prev, .next {
    font-size: 1.2rem;
    padding: 8px 12px;
  }
}

.gallery-item {
  position: relative; 
  background-color: #FFF;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
.gallery-item.horizontal {
  grid-column: span 2;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.caption {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding: 0.5rem;
  background-color: rgba(0, 0, 0, 0.342); 
  color: white; 
  font-size: 0.9rem;
  text-align: center;
  opacity: 0; 
  transition: opacity 0.3s ease;
  align-content: center;
}

.gallery-item:hover .caption {
  opacity: 1; 
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.modal-content {
  background: #fff;
  padding: 2.5rem 2rem 2rem 2rem;
  border-radius: 12px;
  max-width: 800px;
  min-width: 400px;
  width: 60vw;
  box-shadow: 0 2px 20px rgba(0,0,0,0.2);
  text-align: center;
  position: relative;
}
.close-x {
  position: absolute;
  top: 18px;
  right: 22px;
  background: none;
  border: none;
  font-size: 2rem;
  color: #333;
  cursor: pointer;
  z-index: 2;
}
.close-x:hover {
  color: #e74c3c;
}
.defition{
  margin-bottom: 1rem;
  font-weight: bold;
  font-size: 24px;
}

.loading-modal-content {
  background: #fff;
  padding: 2rem 2.5rem;
  border-radius: 12px;
  min-width: 300px;
  max-width: 400px;
  width: 30vw;
  box-shadow: 0 2px 20px rgba(0,0,0,0.2);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.spinner {
  border: 6px solid #f3f3f3;
  border-top: 6px solid #333;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}
@keyframes spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}

</style>
