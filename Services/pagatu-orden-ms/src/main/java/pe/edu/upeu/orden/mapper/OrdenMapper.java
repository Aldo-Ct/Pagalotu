package pe.edu.upeu.orden.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import pe.edu.upeu.orden.dto.OrdenRequest;
import pe.edu.upeu.orden.dto.OrdenResponse;
import pe.edu.upeu.orden.entity.Orden;

@Mapper(componentModel = "spring", uses = OrdenDetalleMapper.class)
public interface OrdenMapper {

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "fechaCreacion", ignore = true)
    @Mapping(target = "estado", ignore = true)
    @Mapping(target = "total", ignore = true)
    Orden toEntity(OrdenRequest request);

    OrdenResponse toResponse(Orden orden);
}
