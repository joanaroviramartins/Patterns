<template>
<div class="container" ref="mainContainer">
    <section class="section" id="home">
      <h1 class="title">
        <span id="">PATTERNS</span>
      </h1>
      <div class="arrow" @click="scrollToGallery">▼</div>
    </section>
    <section class="section" id="gallery">
      <div class="gallery-header">
        <h1 class="gallery-title">GALLERY</h1>
        <input
          class="search-bar"
          id="searchBox"
          placeholder="FILTER THE WORKS BY CONCEPTS"
          type="text"
          @keyup.enter="readingFile"
        />
      </div>
      <div class="gallery-grid-container">
        <div class="gallery-grid">
          <div v-for="(image, index) in filteredImages" 
              :key="index" 
              :class="['gallery-item-gallery', image.orientation, { selected: isSelected(image) }]" 
              @click="handleImageClick(image)">
            <input class="myCheckbox" type="checkbox" :checked="isSelected(image)" />
            <img :src="`http://127.0.0.1:5000/${image.path}`" :alt="image.filename" />
            <div class="keywords">
              <input class="keyword-input" placeholder="Add keyword" type="text"/>
              <button class="add-keyword-button">Submit</button>
            </div>
          </div>
        </div>
      </div>
      <div class="footer">
        <div class="progress">
          <div class="navigationGeneral">
            <span class="nav-circle active"></span>
            <span class="nav-line"></span>
            <span class="nav-circle" @click="readingFile"></span>
            <span class="nav-line"></span>
            <span class="nav-circle" @click="decompose"></span>
            <span class="nav-line"></span>
            <span class="nav-circle"></span>
          </div>
          <div class="navigation-namesGeneral">
            <span class="nav active">GALLERY</span>
            <span class="nav">SELECTED GALLERY</span>
            <span class="nav">UNIT DEVELOPMENT</span>
            <span class="nav">PATTERN</span>
          </div>
        </div>
        <div class="div-arrow">
          <span id="submit">WRITE A CONCEPT OR CHOOSE MANUALLY BEFORE SUBMITTING</span>
          <div class="nav-arrow" @click="readingFile">▶</div>
        </div>
      </div>
    </section>
    <section class="section waiting-overlay" id="waitingGallery" v-if="showWaitingGallery">
      <p class="galleryText">
        While I am selecting the images, take a look at what other users have done!
      </p>
      <div class="slideshow-container">
        <div
          v-for="(img, index) in waitingGalleryImages"
          :key="index"
          class="slide"
          :class="{ active: index === currentSlideIndex }"
        >
          <img
            :src="`http://127.0.0.1:5000/static/waitingGallery/${img}`"
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

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'IndexComponent',
  data() {
    return {
      waitingGalleryImages: [],
        images: [],  
        imagensGaleriaSelecionadas: [], 
        inputword: '',
        userSelectedImages: [],
        showWaitingGallery: false, 
        currentSlideIndex: 0,
        uploadedImages: [], 
        dragOver: false, 
        showRelatedModal: false,
        relatedImages: [],
        filteredImages: [], 
        relatedFilterActive: false, 

    };
  },
  methods: {
    scrollToGallery() {
      const gallerySection = document.getElementById("gallery");
      gallerySection.scrollIntoView({ behavior: "smooth" });
    },
    
    async readingFile() {
      const searchBox = document.getElementById("searchBox");
      
      this.inputword = searchBox.value; 
      this.userSelectedImages = this.imagensGaleriaSelecionadas.map(
        (image) => image.filename
      );
      if (searchBox.value.trim() === "") {
        alert("You have to type in some word(s) to search for works.");
        return;
      } else {
        this.showWaitingGallery = true;
      }

      axios
        .get("http://127.0.0.1:5000/receber-dados", {
          params: {
            inputword: this.inputword,
            userSelectedImages: JSON.stringify(this.userSelectedImages),
          },
        })
        .then((response) => {
          if (response.data.success) {            
            const { relatedWords, selectedImages, userSelectedImages, searchTerm } = response.data;

            this.$router.push({
              path: '/selectedGallery',
              query: {
                searchTerm: JSON.stringify(searchTerm),
                userSelectedImages: JSON.stringify(userSelectedImages),
                relatedWords: JSON.stringify(relatedWords),
                selectedImages: JSON.stringify(selectedImages),
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
    decompose() {
      const imagensSelecionadas = []; 
      if (imagensSelecionadas.length === 0) {
        alert(
          "You have to choose the works you want to decompose by clicking on them."
        );
        return;
      }

      const termSearched = "example"; 
      const semanticSpaceWords = "example"; 
      const transparency = Math.floor(Math.random() * (128 - 4)) + 4;
      const value_cor = Math.floor(Math.random() * (128 - 4)) + 4;
      const rhythm = Math.floor(Math.random() * (128 - 4)) + 4;
      const scale = Math.floor(Math.random() * (254 - 128)) + 127;
      const space = Math.floor(Math.random() * (254 - 128)) + 127;
      const concentration = Math.floor(Math.random() * (128 - 4)) + 4;

      const url = `/decompor?searchTerm=${encodeURIComponent(
        JSON.stringify(termSearched)
      )}&semanticWords=${encodeURIComponent(
        JSON.stringify(semanticSpaceWords)
      )}&selectImages=${encodeURIComponent(
        JSON.stringify(imagensSelecionadas)
      )}&concentration=${encodeURIComponent(
        concentration
      )}&scale=${encodeURIComponent(scale)}&space=${encodeURIComponent(
        space
      )}&rhythm=${encodeURIComponent(rhythm)}&transparency=${encodeURIComponent(
        transparency
      )}&value_cor=${encodeURIComponent(value_cor)}`;

      window.location.href = url;
    },
    scrollToWaiting() {
    },
    isSelected(image, isUploaded = false) {
      if (this.selectedGalleryTab === 'sebastiao' && isUploaded) return false;
      if (this.selectedGalleryTab === 'my' && !isUploaded) return false;
      if (isUploaded) {
        return this.imagensGaleriaSelecionadas.some(
          (item) => item.isUploaded && item.filename === image.filename
        );
      }
      return this.imagensGaleriaSelecionadas.some(
        (item) => !item.isUploaded && item.filename === image.filename
      );
    },
    handleImageClick(image, isUploaded = false) {
      if (this.selectedGalleryTab === 'sebastiao' && isUploaded) return;
      if (this.selectedGalleryTab === 'my' && !isUploaded) return;
      const isSelected = this.isSelected(image, isUploaded);

      if (isSelected) {
        this.imagensGaleriaSelecionadas = this.imagensGaleriaSelecionadas.filter(
          (item) =>
            (item.isUploaded !== isUploaded) ||
            (item.filename !== image.filename)
        );
      } else {
        this.imagensGaleriaSelecionadas.push({ ...image, isUploaded });
      }
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
    preventScrollToWaiting(e) {
      if (this.showWaitingGallery) {
        e.preventDefault();
      }
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
  mounted() {
    axios.get('http://127.0.0.1:5000/api/images')
      .then(response => {
        this.images = response.data.images;
        this.filteredImages = this.images; 
      })
      .catch(error => {
        console.error('Error fetching images:', error);
      });

    document.addEventListener('wheel', this.preventScrollToWaiting, { passive: false });
    document.addEventListener('touchmove', this.preventScrollToWaiting, { passive: false });
    this.fetchWaitingGallery();

  },
  beforeUnmount() {
    document.removeEventListener('wheel', this.preventScrollToWaiting);
    document.removeEventListener('touchmove', this.preventScrollToWaiting);
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@400;600;700&display=swap");
@import "@/assets/style2.css"; 

.container {
  height: 100vh;
  overflow-y: auto;
  scroll-snap-type: y mandatory;
}

.section {
  scroll-snap-align: start;
  min-height: 100vh;
}

.gallery-item-gallery {
  border-radius: 6px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Overlay for waiting gallery */
.waiting-overlay {
  position: fixed !important;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: 9999;
  background: #F9F5EF;
  overflow: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.upload-btn {
  margin-left: 10px;
  padding: 6px 16px;
  background: #333;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.upload-btn:hover {
  background: #555;
}
.uploaded-label {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #e0e0e0;
  color: #333;
  font-size: 0.7em;
  padding: 2px 6px;
  border-radius: 4px;
  pointer-events: none;
}
.gallery-tabs {
  display: flex;
  width: 95%;
  gap: 1rem;
  display: none;
}

.tabs {
  display: flex;
  gap: 18px;
  margin-top: 0.2em;
  margin-bottom: 1.2em;
  justify-content: flex-start;
}

.gallery-tab {
  background: none;
  border: none;
  font-size: 0.97em;
  font-family: inherit;
  color: #a67e6675; 
  padding: 0 0 2px 0;
  margin: 0;
  cursor: pointer;
  transition: color 0.2s, border-bottom 0.2s;
  font-weight: 600;
  outline: none;
}

.gallery-tab.active {
  color: #A67E66; 
  font-weight: 700;
}

.gallery-tab:not(.active):hover {
  color: #a67e66a7;
}

.gallery-grid-container.drag-over {
  border: 2px dashed #a67e6675;
  background: #a67e6675;
}
.drag-drop-hint {
  margin-top: 15rem;
}

.my-gallery-dropzone {
  width: 95%;
  height: 71vh;
  overflow-y: auto;
  display: flex;
  justify-content: center;
}
.my-gallery-dropzone.drag-over {
  border-color: #A67E66;
  background: #f3ede5;
}
.dropzone-content-centered {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  width: 100%;
  height: 220px;
  text-align: center;
  user-select: none;
}
.dropzone-icon {
  margin-bottom: 16px;
}
.dropzone-text-centered {
  color: #a67e66;
  font-size: 1.15em;
  font-weight: 500;
}
.upload-link {
  color: #A67E66;
  text-decoration: underline;
  cursor: pointer;
  font-weight: 600;
}
.my-gallery-dropzone .gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(20%, 1fr));
  gap: 0.5rem;
  width: 100%;
  padding-right: 0.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
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
@media (max-width: 1024px) {
  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}

@media (max-width: 768px) {
  /* Hero */
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
  .title {
    font-size: 3rem;
  }

  .gallery-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .search-bar {
    width: 100%; 
  }

  /* Grid */
  .gallery-grid {
    grid-template-columns: repeat(2, 1fr); 
    gap: 10px;
  }

  .footer {
    padding: 15px;
  }
  
  .navigation-namesGeneral {
    font-size: 0.6rem; 
    flex-wrap: wrap;
    gap: 5px;
  }
  
  .div-arrow {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }

  .slideshow-container {
    max-width: 90%; 
  }
  
  .prev, .next {
    font-size: 1.5rem;
    padding: 5px 10px;
  }
  
  .galleryText {
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 2.5rem;
  }


  .navigation-namesGeneral {
    display: none; 
  }
  
  .navigationGeneral {
    margin-bottom: 10px;
  }
}

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
#waitingGallery {
  background: #F9F5EF;
  padding: 30px 20px;
}

.galleryText {
  font-size: 25px;
margin-top: 3%;
}

@keyframes fade {
  from {opacity: .4} 
  to {opacity: 1}
}

</style>