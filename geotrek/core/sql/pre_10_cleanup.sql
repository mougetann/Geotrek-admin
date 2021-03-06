-- 10

DROP FUNCTION IF EXISTS ST_InterpolateAlong(geometry, geometry) CASCADE;
DROP FUNCTION IF EXISTS ST_Smart_Line_Substring(geometry, float, float) CASCADE;
DROP FUNCTION IF EXISTS ST_SmartLineSubstring(geometry, float, float) CASCADE;
DROP FUNCTION IF EXISTS ft_IsBefore(geometry, geometry) CASCADE;
DROP FUNCTION IF EXISTS ft_IsAfter(geometry, geometry) CASCADE;
DROP FUNCTION IF EXISTS ft_Smart_MakeLine(geometry[]) CASCADE;

-- 20

DROP INDEX IF EXISTS evenements_geom_idx;
DROP INDEX IF EXISTS e_t_evenement_geom_idx;
DROP INDEX IF EXISTS core_topology_geom_idx;

DROP FUNCTION IF EXISTS evenement_latest_updated_d() CASCADE;
DROP FUNCTION IF EXISTS topology_latest_updated_d() CASCADE;

DROP FUNCTION IF EXISTS update_geometry_of_evenement(integer) CASCADE;
DROP FUNCTION IF EXISTS update_geometry_of_topology(integer) CASCADE;

DROP FUNCTION IF EXISTS update_evenement_geom_when_offset_changes() CASCADE;
DROP FUNCTION IF EXISTS update_topology_geom_when_offset_changes() CASCADE;

DROP FUNCTION IF EXISTS evenement_elevation_iu() CASCADE;
DROP FUNCTION IF EXISTS topology_elevation_iu() CASCADE;

-- 30

DROP FUNCTION IF EXISTS ft_troncon_interpolate(integer, geometry) CASCADE;
DROP FUNCTION IF EXISTS ft_path_interpolate(integer, geometry) CASCADE;

DROP FUNCTION IF EXISTS ft_evenements_troncons_geometry() CASCADE;
DROP FUNCTION IF EXISTS ft_topologies_paths_geometry() CASCADE;

DROP FUNCTION IF EXISTS ft_evenements_troncons_junction_point_iu() CASCADE;
DROP FUNCTION IF EXISTS ft_topologies_paths_junction_point_iu() CASCADE;

-- 40

DROP INDEX IF EXISTS troncons_geom_idx;
DROP INDEX IF EXISTS l_t_troncon_geom_idx;
DROP INDEX IF EXISTS core_path_geom_idx;

DROP INDEX IF EXISTS troncons_start_point_idx;
DROP INDEX IF EXISTS l_t_troncon_start_point_idx;
DROP INDEX IF EXISTS core_path_start_point_idx;

DROP INDEX IF EXISTS troncons_end_point_idx;
DROP INDEX IF EXISTS l_t_troncon_end_point_idx;
DROP INDEX IF EXISTS core_path_end_point_idx;

DROP INDEX IF EXISTS troncons_geom_cadastre_idx;
DROP INDEX IF EXISTS l_t_troncon_geom_cadastre_idx;
DROP INDEX IF EXISTS core_path_geom_cadastre_idx;

DROP INDEX IF EXISTS l_t_troncon_geom_3d_idx;
DROP INDEX IF EXISTS core_path_geom_3d_idx;

DROP FUNCTION IF EXISTS check_path_not_overlap(integer, geometry) CASCADE;

DROP FUNCTION IF EXISTS update_evenement_geom_when_troncon_changes() CASCADE;
DROP FUNCTION IF EXISTS update_topology_geom_when_path_changes() CASCADE;

DROP FUNCTION IF EXISTS elevation_troncon_iu() CASCADE;
DROP FUNCTION IF EXISTS elevation_path_iu() CASCADE;

DROP FUNCTION IF EXISTS troncons_related_objects_d() CASCADE;
DROP FUNCTION IF EXISTS paths_related_objects_d() CASCADE;

DROP FUNCTION IF EXISTS troncon_latest_updated_d() CASCADE;
DROP FUNCTION IF EXISTS path_latest_updated_d() CASCADE;

-- 50

DROP FUNCTION IF EXISTS troncons_snap_extremities() CASCADE;
DROP FUNCTION IF EXISTS paths_snap_extremities() CASCADE;

DROP FUNCTION IF EXISTS troncons_evenement_intersect_split() CASCADE;
DROP FUNCTION IF EXISTS paths_topology_intersect_split() CASCADE;

-- 60

DROP VIEW IF EXISTS l_v_sentier CASCADE;
DROP VIEW IF EXISTS v_trails CASCADE;

-- 70

DROP FUNCTION IF EXISTS ft_merge_path(integer,integer) CASCADE;
