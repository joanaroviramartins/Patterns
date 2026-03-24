import { createRouter, createWebHistory } from 'vue-router'; 
import IndexComponent from '@/views/IndexComponent.vue';
import SelectedGallery from '@/views/SelectedGallery.vue';
import UnitDevelopment from '@/views/UnitDevelopment.vue';
import PatternDevelopment from '@/views/PatternDevelopment.vue';


const routes = [
  {
    path: '/',
    name: 'IndexComponent',
    component: IndexComponent,
  },
  {
    path: '/selectedGallery', 
    name: 'SelectedGallery',
    component: SelectedGallery,
  },
  {
    path: '/unit', 
    name: 'UnitDevelopment',
    component: UnitDevelopment,
  },
  {
    path: '/pattern',
    name: 'PatternDevelopment',
    component: PatternDevelopment,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
