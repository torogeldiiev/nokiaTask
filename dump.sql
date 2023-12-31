PGDMP     $            
        {            movies    15.2    15.2                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16464    movies    DATABASE     z   CREATE DATABASE movies WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE movies;
                postgres    false            �            1259    16553    moviepeople    TABLE     c   CREATE TABLE public.moviepeople (
    movie_id integer NOT NULL,
    person_id integer NOT NULL
);
    DROP TABLE public.moviepeople;
       public         heap    postgres    false            �            1259    16542    movies    TABLE     �   CREATE TABLE public.movies (
    movie_id integer NOT NULL,
    title character varying(255) NOT NULL,
    director_id integer,
    release_year integer,
    length_minutes integer
);
    DROP TABLE public.movies;
       public         heap    postgres    false            �            1259    16541    movies_movie_id_seq    SEQUENCE     �   CREATE SEQUENCE public.movies_movie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.movies_movie_id_seq;
       public          postgres    false    217                       0    0    movies_movie_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.movies_movie_id_seq OWNED BY public.movies.movie_id;
          public          postgres    false    216            �            1259    16535    people    TABLE     �   CREATE TABLE public.people (
    person_id integer NOT NULL,
    name character varying(255) NOT NULL,
    birth_year integer,
    is_director boolean DEFAULT false,
    is_actor boolean DEFAULT true
);
    DROP TABLE public.people;
       public         heap    postgres    false            �            1259    16534    people_person_id_seq    SEQUENCE     �   CREATE SEQUENCE public.people_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.people_person_id_seq;
       public          postgres    false    215                       0    0    people_person_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.people_person_id_seq OWNED BY public.people.person_id;
          public          postgres    false    214            q           2604    16545    movies movie_id    DEFAULT     r   ALTER TABLE ONLY public.movies ALTER COLUMN movie_id SET DEFAULT nextval('public.movies_movie_id_seq'::regclass);
 >   ALTER TABLE public.movies ALTER COLUMN movie_id DROP DEFAULT;
       public          postgres    false    217    216    217            n           2604    16538    people person_id    DEFAULT     t   ALTER TABLE ONLY public.people ALTER COLUMN person_id SET DEFAULT nextval('public.people_person_id_seq'::regclass);
 ?   ALTER TABLE public.people ALTER COLUMN person_id DROP DEFAULT;
       public          postgres    false    214    215    215                      0    16553    moviepeople 
   TABLE DATA           :   COPY public.moviepeople (movie_id, person_id) FROM stdin;
    public          postgres    false    218   �                 0    16542    movies 
   TABLE DATA           \   COPY public.movies (movie_id, title, director_id, release_year, length_minutes) FROM stdin;
    public          postgres    false    217          
          0    16535    people 
   TABLE DATA           T   COPY public.people (person_id, name, birth_year, is_director, is_actor) FROM stdin;
    public          postgres    false    215   �                  0    0    movies_movie_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.movies_movie_id_seq', 9, true);
          public          postgres    false    216                       0    0    people_person_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.people_person_id_seq', 31, true);
          public          postgres    false    214            w           2606    16559    moviepeople moviepeople_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public.moviepeople
    ADD CONSTRAINT moviepeople_pkey PRIMARY KEY (movie_id, person_id);
 F   ALTER TABLE ONLY public.moviepeople DROP CONSTRAINT moviepeople_pkey;
       public            postgres    false    218    218            u           2606    16547    movies movies_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (movie_id);
 <   ALTER TABLE ONLY public.movies DROP CONSTRAINT movies_pkey;
       public            postgres    false    217            s           2606    16540    people people_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.people
    ADD CONSTRAINT people_pkey PRIMARY KEY (person_id);
 <   ALTER TABLE ONLY public.people DROP CONSTRAINT people_pkey;
       public            postgres    false    215            y           2606    16560 %   moviepeople moviepeople_movie_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.moviepeople
    ADD CONSTRAINT moviepeople_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(movie_id);
 O   ALTER TABLE ONLY public.moviepeople DROP CONSTRAINT moviepeople_movie_id_fkey;
       public          postgres    false    218    3189    217            z           2606    16565 &   moviepeople moviepeople_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.moviepeople
    ADD CONSTRAINT moviepeople_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.people(person_id);
 P   ALTER TABLE ONLY public.moviepeople DROP CONSTRAINT moviepeople_person_id_fkey;
       public          postgres    false    218    3187    215            x           2606    16548    movies movies_director_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_director_id_fkey FOREIGN KEY (director_id) REFERENCES public.people(person_id);
 H   ALTER TABLE ONLY public.movies DROP CONSTRAINT movies_director_id_fkey;
       public          postgres    false    217    3187    215               2   x�3�4�2�4bc.#N 6�2��`ڌ�(gTc�ih $L�b���� �p�         y   x�3�t�J�K�W�K�H��KM�4�4204�443�2�(�)Pp�L.����ZZ	S.CNϼ�����!�!H�������X�H�pYrgd��+�d�p�C%��b���� �"�      
   �   x�]�Mn� ��p�9A���:YTQT)���fҎc�������}o�y���O�Gs�5�ok� �
Fo�%��ۂ{�n��y�'��?�Kaݕ��7K8�[�������!K��5�DZ�g�eH����0�~�9�_�vF�D��]4G
��yS=��0D�b��jx�r��M��;�&R}ߧC�������9a�,��B�Z�M     