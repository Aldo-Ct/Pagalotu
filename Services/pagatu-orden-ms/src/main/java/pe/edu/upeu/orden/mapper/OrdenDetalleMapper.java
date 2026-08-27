package pe.edu.upeu.orden.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import pe.edu.upeu.orden.dto.OrdenDetalleRequest;
import pe.edu.upeu.orden.dto.OrdenDetalleResponse;
import pe.edu.upeu.orden.entity.OrdenDetalle;

@Mapper(componentModel = "spring")
public interface OrdenDetalleMapper {

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "orden", ignore = true)
    OrdenDetalle toEntity(OrdenDetalleRequest request);

    OrdenDetalleResponse toResponse(OrdenDetalle detalle);
}
