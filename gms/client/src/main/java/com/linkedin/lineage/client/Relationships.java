package com.linkedin.lineage.client;

import com.linkedin.common.EntityRelationships;
import com.linkedin.common.client.BaseClient;
import com.linkedin.lineage.RelationshipsRequestBuilders;
import com.linkedin.metadata.query.RelationshipDirection;
import com.linkedin.r2.RemoteInvocationException;
import com.linkedin.restli.client.Client;
import com.linkedin.restli.client.GetRequest;

import javax.annotation.Nonnull;
import java.net.URISyntaxException;

public class Relationships extends BaseClient {

    public Relationships(@Nonnull Client restliClient) {
        super(restliClient);
    }
    private static final RelationshipsRequestBuilders RELATIONSHIPS_REQUEST_BUILDERS =
            new RelationshipsRequestBuilders();

    /**
     * Gets a specific version of downstream {@link EntityRelationships} for the given dataset.
     */
    @Nonnull
    public EntityRelationships getRelationships(@Nonnull String rawUrn, @Nonnull RelationshipDirection direction, @Nonnull String types)
            throws RemoteInvocationException, URISyntaxException {

        final GetRequest<EntityRelationships> request = RELATIONSHIPS_REQUEST_BUILDERS.get()
                .urnParam(rawUrn)
                .directionParam(direction.toString())
                .typesParam(types)
                .build();
        return _client.sendRequest(request).getResponseEntity();
    }
}
